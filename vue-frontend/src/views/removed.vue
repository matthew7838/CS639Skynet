<template>
  <div>
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
          <el-menu-item index="/ucs_removed">
              <i class="el-icon-delete"></i>
              UCS Removed
          </el-menu-item>
          <el-menu-item index="/version">
            <i class="el-icon-date"></i>
            <span slot="title">Version Control</span>
          </el-menu-item>
          <el-submenu index="2">
            <template slot="title">
              <i class="el-icon-download"></i>
              <span>Export</span>
            </template>
            <el-menu-item @click.native="exportData('pdf')">
              <i class="el-icon-notebook-2"></i>
              Export to Excel
            </el-menu-item>
            <el-menu-item @click.native="exportData('excel')">
              <i class="el-icon-document"></i>
              Export to PDF
            </el-menu-item>
            <el-menu-item @click.native="exportData('csv')">
              <i class="el-icon-document-copy"></i>
              Export to CSV
            </el-menu-item>
          </el-submenu>
          <el-menu-item @click="logout">
            <i class="el-icon-switch-button"></i>
            <span slot="title">Logout</span>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <el-container>
        <!--        Header-->
        <el-header>

          <el-breadcrumb style="margin-left: 20px">
            <el-breadcrumb-item>Welcome, {{ username }}!</el-breadcrumb-item>
          </el-breadcrumb>

          <!--          <i :class="collapseIcon" style="font-size: 26px" @click="handleCollapse"></i>-->
          <el-breadcrumb separator-class="el-icon-arrow-right" style="margin-left: 20px">
            <el-breadcrumb-item :to="{ path: '/' }">Remove Page</el-breadcrumb-item>
          </el-breadcrumb>

          <!-- Search input for satellite name -->
          <el-input v-model="searchQuery" placeholder="Search by Satellite Name" style="width: 300px; margin-left: 20px;">
          </el-input>
        </el-header>

        <!--        Main Page-->
        <el-main>
          <el-table :data="filteredData" style="width: 100%">
            <el-table-column fixed prop="full_name" label="full_name" width="200"></el-table-column>
            <el-table-column prop="official_name" label="official_name" width="150"></el-table-column>
            <el-table-column v-for="column in editColumns" :key="column" :prop="column" :label="column" width="200">
            </el-table-column>
            <el-table-column prop="data_status" label="data_status" width="350"></el-table-column>
            <el-table-column v-for="column in dynamicColumns" :key="column" :prop="column" :label="column" width="350">
            </el-table-column>
            <el-table-column prop="additional_source" label="additional_source" width="350"></el-table-column>
            <el-table-column fixed="right" prop="removal_reason" label="Reason" width="200"></el-table-column>
            <el-table-column fixed="right" label="Operations" width="120">
              <template slot-scope="scope">
                <el-button type="danger" icon="el-icon-delete" size="mini" @click="removeRow(scope.$index, scope.row)">
                  Delete
                </el-button>
              </template>
            </el-table-column>

          </el-table>

          <!-- Removed Items Table -->
          <el-table :data="removedItems" style="width: 100%; margin-top: 30px;" v-if="removedItems.length > 0">
            <el-table-column fixed prop="full_name" label="full_name" width="250"></el-table-column>
            <el-table-column fixed prop="official_name" label="official_name" width="150"></el-table-column>
            <el-table-column v-for="column in editColumns" :key="column" :prop="column" :label="column" width="200">
            </el-table-column>
            <el-table-column prop="data_status" label="data_status" width="350"></el-table-column>
            <el-table-column v-for="column in dynamicColumns" :key="column" :prop="column" :label="column" width="350">
            </el-table-column>
            <el-table-column prop="additional_source" label="additional_source" width="350"></el-table-column>
            <el-table-column fixed="right" prop="removal_reason" label="Reason" width="200"></el-table-column>
            <el-table-column fixed="right" label="Operations" width="120">
              <template slot-scope="scope">
                <el-button type="primary" icon="el-icon-refresh" size="mini" @click="undoRemove(scope.$index, scope.row)">
                  Undo
                </el-button>
              </template>
            </el-table-column>
          </el-table>

        </el-main>

        <div style="display: flex; justify-content: center; align-items: center; margin-top: 30px; padding: 20px;">
          <el-button type="success" @click="publishChanges">Publish Changes</el-button>
        </div>
      </el-container>
      <!-- Section for publishing changes -->
    </el-container>
  </div>
</template>
  
<script>
import axios from "axios";
export default {
  data() {
    return {
      isCollapse: false,
      asideWidth: "200px",
      collapseIcon: "el-icon-s-fold",
      tableData: [],
      removedItems: [],
      searchQuery: '',
      username: '',
      columns: [], // This now includes all columns
      dynamicColumns: [],
      editColumns: []
    };
  },
  mounted() {
    this.fetchRemovedSatellites();
    this.getUsername();
  },
  computed: {
    // Add a computed property for filtering data
    filteredData() {
      if (this.searchQuery) {
        return this.tableData.filter(item =>
          item.satellite_name.toLowerCase().includes(this.searchQuery.toLowerCase())
        );
      }
      return this.tableData;
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
    async fetchRemovedSatellites() {
      try {
        const response = await axios.get("http://localhost:8000/api/removed");
        this.tableData = response.data;
        if (this.tableData.length > 0) {
          const allColumns = Object.keys(this.tableData[0]);
          this.dynamicColumns = allColumns.filter(col => col.startsWith('source'));
          this.manualColumns = ['additional_source', 'full_name', 'official_name', 'editing', 'country', 'data_status', 'removal_reason'];

          // Define editColumns as all columns that are not dynamic or manual
          this.editColumns = allColumns.filter(col =>
            !this.dynamicColumns.includes(col) && !this.manualColumns.includes(col)
          );
        }
        console.log(this.tableData);
      } catch (error) {
        console.error("There was an error fetching the data:", error);
      }
    },
    removeRow(index, row) {
      this.removedItems.push(row); // Add the row to the removed items
      this.tableData.splice(index, 1); // Remove the row from the main table
      // You may also want to handle the removal in your backend/database
    },
    undoRemove(index, row) {
      this.tableData.push(row); // Add the row back to the main table
      this.removedItems.splice(index, 1); // Remove the row from the removed items
      // You may also want to handle the restoration in your backend/database
    },
    tableRowClassName({ row, rowIndex }) {
      // Here, you can specify a condition to highlight rows that need attention
      if (rowIndex === 2) {
        return 'highlight-row';
      }
      return '';
    },
    publishChanges() {

      // Update data_status for all removed items
      let cospar_list = this.removedItems.map(item => item.cospar);

      console.log(cospar_list)

      // Send the updated items and publisher name to the backend for database update
      axios.post('http://localhost:8000/api/update-status', {
        cospar_list: cospar_list,
        name: this.username  // Include the username in the request payload
      })
        .then(response => {
          console.log(response.data);
          // Handle the response, e.g., show a success message
          this.$message.success('Changes have been published successfully.');

          // Clear the removedItems if they have been successfully published
          this.removedItems = [];
        })
        .catch(error => {
          console.error('There was an error publishing the changes:', error);
          // Handle the error, e.g., show an error message
          this.$message.error('Failed to publish changes.');
        });

    },
  },
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
  