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
                <el-menu-item index="/">
                    <i class="el-icon-house"></i>
                    <span slot="title">Home Page</span>
                </el-menu-item>
                <el-menu-item index="/edit">
                    <i class="el-icon-time"></i>
                    <span slot="title">Edit History</span>
                </el-menu-item>
                <el-menu-item index="/removed">
                    <i class="el-icon-delete"></i>
                    <span slot="title">Removed</span>
                </el-menu-item>
                <el-menu-item index="/history">
                    <i class="el-icon-time"></i>
                    <span slot="title">History</span>
                </el-menu-item>
            </el-menu>
        </el-aside>

        <el-container>
            <!--    Main Page-->
            <!--        Header-->
            <el-header>
                <!--          <i :class="collapseIcon" style="font-size: 26px" @click="handleCollapse"></i>-->
                <el-breadcrumb separator-class="el-icon-arrow-right" style="margin-left: 20px">
                    <el-breadcrumb-item :to="{ path: '/' }">History Page</el-breadcrumb-item>
                </el-breadcrumb>
            </el-header>
            <el-main>
                <el-table :data="historyData" style="width: 100%">
                    <el-table-column prop="name" label="Name"></el-table-column>
                    <el-table-column prop="date" label="Date" width="180"></el-table-column>
                    <el-table-column label="Operations" width="100">
                        <template slot-scope="scope">
                            <el-button type="text" size="small" @click="showDetails(scope.row)">Show</el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </el-main>
            <!-- Add a modal dialog for showing JCAT details -->
            <el-dialog :visible.sync="showJCATModal" title="JCAT Details">
                <el-table :data="jcatDetails" style="width: 100%">
                    <el-table-column fixed prop="satellite_name" label="satellite_name"></el-table-column>
                    <el-table-column prop="un_registry_country" label="un_registry_country"></el-table-column>
                    <el-table-column prop="operator_country" label="operator_country"></el-table-column>
                    <el-table-column prop="operator" label="operator"></el-table-column>
                    <el-table-column prop="user_type" label="user_type"></el-table-column>
                    <el-table-column prop="purpose" label="purpose"></el-table-column>
                    <el-table-column prop="detailed_purpose" label="detailed_purpose"></el-table-column>
                    <el-table-column prop="orbit_class" label="orbit_class"></el-table-column>
                    <el-table-column prop="orbit_type" label="orbit_type"></el-table-column>
                    <el-table-column prop="longitude_geo" label="longitude_geo"></el-table-column>
                    <el-table-column prop="perigee" label="perigee"></el-table-column>
                    <el-table-column prop="apogee" label="apogee" width="150"></el-table-column>
                    <el-table-column prop="eccentricity" label="eccentricity" width="150"></el-table-column>
                    <el-table-column prop="inclination" label="inclination" width="150"></el-table-column>
                    <el-table-column prop="orbital_period" label="orbital_period" width="150"></el-table-column>
                    <el-table-column prop="launch_mass" label="launch_mass" width="150"></el-table-column>
                    <el-table-column prop="dry_mass" label="dry_mass" width="150"></el-table-column>
                    <el-table-column prop="power" label="power" width="150"></el-table-column>
                    <el-table-column prop="launch_date" label="launch_date" width="150"></el-table-column>
                    <el-table-column prop="lifetime" label="lifetime" width="150"></el-table-column>
                    <el-table-column prop="contractor" label="contractor" width="150"></el-table-column>
                    <el-table-column prop="contractor_country" label="contractor_country" width="150"></el-table-column>
                    <el-table-column prop="launch_site" label="launch_site" width="150"></el-table-column>
                    <el-table-column prop="launch_vehicle" label="launch_vehicle" width="150"></el-table-column>
                    <el-table-column prop="cospar" label="cospar" width="150"></el-table-column>
                    <el-table-column prop="norad" label="norad" width="150"></el-table-column>
                    <el-table-column prop="comments" label="comments" width="150"></el-table-column>
                    <el-table-column prop="orbital_data_source" label="orbital_data_source" width="150"></el-table-column>
                    <el-table-column prop="source1" label="source1" width="150"></el-table-column>
                    <el-table-column prop="data_status" label="data_status" width="150"></el-table-column>
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
            jcatDetails: [],
        };
    },
    mounted() {
        this.fetchHistory();
    },
    methods: {
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
                const response = await axios.get(`http://localhost:8000/api/history/details?name=${row.name}&date=${row.date}`);
                // Set the JCAT details to a data property and open the modal
                this.jcatDetails = response.data;
                this.showJCATModal = true;
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
</style>

  