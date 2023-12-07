<template>
    <el-container>
        <!--    SideBar  -->
        <el-aside :width="asideWidth" style="min-height: 100vh; background-color: #001529">
            <div style="
                                        height: 60px;
                                        color: white;
                                        display: flex;
                                        align-items: center;
                                        justify-content: center;
                                    ">
                <img src="@/assets/UCS-Logo.png" alt="" style="width: 120px; height: 60px" />
            </div>

            <el-menu :collapse="isCollapse" :collapse-transition="false" router background-color="#001529"
                text-color="rgba(255, 255, 255, 0.65)" active-text-color="#fff" style="border: none"
                :default-active="$route.path">
                <!-- Master Database Submenu -->
                <el-submenu index="1">
                    <template slot="title">
                        <i class="el-icon-menu"></i>
                        <span>Master Database</span>
                    </template>
                    <el-menu-item index="/">
                        <i class="el-icon-house"></i>
                        Home Page
                    </el-menu-item>
                    <el-menu-item index="/edit">
                        <i class="el-icon-edit"></i>
                        Edit History
                    </el-menu-item>
                    <el-menu-item index="/removed">
                        <i class="el-icon-delete"></i>
                        Removed
                    </el-menu-item>
                    <el-menu-item index="/history">
                        <i class="el-icon-time"></i>
                        History
                    </el-menu-item>
                </el-submenu>
                <el-menu-item index="/crawler">
                    <i class="el-icon-search"></i>
                    <span slot="title">Crawler</span>
                </el-menu-item>
                <el-menu-item @click="logout">
                    <i class="el-icon-switch-button"></i>
                    <span slot="title">Logout</span>
                </el-menu-item>

            </el-menu>
        </el-aside>

        <el-container>
            <!--    Main Page-->
            <!--        Header-->
            <el-header>

                <el-breadcrumb style="margin-left: 20px">
                    <el-breadcrumb-item>Welcome, {{ username }}!</el-breadcrumb-item>
                </el-breadcrumb>

                <!--          <i :class="collapseIcon" style="font-size: 26px" @click="handleCollapse"></i>-->
                <el-breadcrumb separator-class="el-icon-arrow-right" style="margin-left: 20px">
                    <el-breadcrumb-item :to="{ path: '/' }">History Page</el-breadcrumb-item>
                </el-breadcrumb>
                <!-- Search input for satellite name -->
                <el-input v-model="searchQuery" placeholder="Search by Cospar" style="width: 300px; margin-left: 20px;">
                </el-input>
            </el-header>
            <el-main>
                <el-table :data="filteredData" style="width: 100%">
                    <el-table-column prop="name" label="Name"></el-table-column>
                    <el-table-column prop="date" label="Date" width="180"></el-table-column>
                    <el-table-column fixed prop="cospar" label="cospar"></el-table-column>
                    <el-table-column label="Operations" width="100">
                        <template slot-scope="scope">
                            <el-button type="text" size="small" @click="showDetails(scope.row)">Show</el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </el-main>
            <!-- Add a modal dialog for showing JCAT details -->
            <el-dialog :visible.sync="showJCATModal" title="Satellite Details">
                <el-table :data="tableData" style="width: 100%">
                    <el-table-column fixed prop="full_name" label="full_name" width="150"></el-table-column>
                    <el-table-column prop="official_name" label="official_name" width="150"></el-table-column>
                    <el-table-column v-for="column in editColumns" :key="column" :prop="column" :label="column" width="200">
                    </el-table-column>
                    <el-table-column prop="data_status" label="data_status" width="350"></el-table-column>
                    <el-table-column v-for="column in dynamicColumns" :key="column" :prop="column" :label="column"
                        width="350">
                    </el-table-column>
                    <el-table-column prop="additional_source" label="additional_source" width="350"></el-table-column>
                    <el-table-column fixed="right" prop="removal_reason" label="Reason" width="200"></el-table-column>
                </el-table>
                <span slot="footer" class="dialog-footer">
                    <el-button @click="showJCATModal = false">Close</el-button>
                </span>
            </el-dialog>
        </el-container>
    </el-container>
</template>


<script>
import axios from "axios";
export default {
    data() {
        return {
            isCollapse: false,
            asideWidth: "200px",
            historyData: [],
            showJCATModal: false,
            searchQuery: '',
            username: '',
            tableData: [],
            columns: [], // This now includes all columns
            dynamicColumns: [],
            editColumns: []
        };
    },
    mounted() {
        this.fetchHistory();
        this.getUsername();
    },
    computed: {
        // Add a computed property for filtering data
        filteredData() {
            if (this.searchQuery) {
                return this.historyData.filter(item =>
                    item.cospar.toLowerCase().includes(this.searchQuery.toLowerCase())
                );
            }
            return this.historyData;
        },
    },
    methods: {
        logout() {
            localStorage.removeItem('authToken'); // 清除本地存储中的 token
            this.$router.push('/login'); // 重定向到登录页面
        },
        getUsername() {
            // Retrieve the username from local storage
            this.username = localStorage.getItem('username');
            console.log("Retrieved username:", this.username);
        },
        async fetchHistory() {
            try {
                const response = await axios.get(
                    "http://localhost:8000/api/history" // Replace with your actual API endpoint
                );
                this.historyData = response.data;
                console.log(this.historyData);
            } catch (error) {
                console.error("There was an error fetching the history data:", error);
            }
        },
        async showDetails(row) {
            try {
                const url = `http://localhost:8000/api/history/details?cospar=${encodeURIComponent(row.cospar)}`;
                const response = await axios.get(url);  // Add this line to make the API call
                this.tableData = response.data;

                if (this.tableData.length > 0) {
                    const allColumns = Object.keys(this.tableData[0]);
                    this.dynamicColumns = allColumns.filter(col => col.startsWith('source'));
                    this.manualColumns = ['additional_source', 'full_name', 'official_name', 'editing', 'country', 'data_status', 'removal_reason'];

                    this.editColumns = allColumns.filter(col =>
                        !this.dynamicColumns.includes(col) && !this.manualColumns.includes(col)
                    );
                    console.log(this.editColumns);
                }
                this.showJCATModal = true; // Open the modal
            } catch (error) {
                console.error("There was an error fetching the JCAT details:", error);
            }
        }
    }
};
</script>
  

<style>
.el-table {
    margin-top: 20px;
}

.el-menu--inline {
    background-color: #000c17 !important;
}

.el-menu--inline .el-menu-item {
    background-color: #000c17 !important;
    padding-left: 49px !important;
}

.el-menu-item:hover,
.el-submenu__title:hover {
    color: #fff !important;
}

.el-submenu__title:hover i {
    color: #fff !important;
}

.el-menu-item:hover i {
    color: #fff !important;
}

.el-menu-item.is-active {
    background-color: #1890ff !important;
    border-radius: 5px !important;
    width: calc(100% - 8px);
    margin-left: 4px;
}

.el-menu-item.is-active i,
.el-menu-item.is-active .el-tooltip {
    margin-left: -4px;
}

.el-menu-item {
    height: 40px !important;
    line-height: 40px !important;
}

.el-submenu__title {
    height: 40px !important;
    line-height: 40px !important;
}

.el-submenu .el-menu-item {
    min-width: 0 !important;
}

.el-menu--inline .el-menu-item.is-active {
    padding-left: 45px !important;
}

/*.el-submenu__icon-arrow {*/
/*  margin-top: -5px;*/
/*}*/

.el-aside {
    transition: width 0.3s;
    box-shadow: 2px 0 6px rgba(0, 21, 41, 0.35);
}

.logo-title {
    margin-left: 5px;
    font-size: 20px;
    transition: all 0.3s;
    /* 0.3s */
}

.el-header {
    box-shadow: 2px 0 6px rgba(0, 21, 41, 0.35);
    display: flex;
    align-items: center;
}

.no-transition-submenu .el-menu--collapse {
    transition: none !important;
}
</style>

  