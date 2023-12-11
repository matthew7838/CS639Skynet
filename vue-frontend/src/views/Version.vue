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
            <el-menu-item @click.native="exportData('excel')">
              <i class="el-icon-notebook-2"></i>
              Export to Excel
            </el-menu-item>
            <el-menu-item @click.native="exportData('pdf')">
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
            <el-breadcrumb-item :to="{ path: '/' }">Edit Page</el-breadcrumb-item>
          </el-breadcrumb>

          <!-- Search input for satellite name -->
          <el-input v-model="searchQuery" placeholder="Search by Satellite Name"
                    style="width: 300px; margin-left: 20px;">
          </el-input>
        </el-header>

        <!--        Main Page-->
        <el-main>
          <el-table :data="versionData" style="width: 100%">
            <el-table-column prop="version" label="Version"></el-table-column>
            <el-table-column prop="timestamp" label="Timestamp"></el-table-column>
            <el-table-column
                label="Operations"
                width="180">
              <template slot-scope="scope">
                <el-button
                    size="mini"
                    @click="rollbackVersion(scope.row)">Rollback
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-main>


      </el-container>

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
      tableData: [],
      searchQuery: '',
      username: '',
      versionData: [],
    };
  },
  mounted() {
    this.fetchEditRecords();
    this.getUsername();
    this.fetchVersionData();
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
      localStorage.removeItem('authToken');
      this.$router.push('/login');
    },
    exportData(format) {
      window.location.href = `http://localhost:8000/api/export/${format}`;
    },
    getUsername() {
      // Retrieve the username from local storage
      this.username = localStorage.getItem('username');
      console.log("Retrieved username:", this.username);
    },
    async fetchEditRecords() {
      try {
        const response = await axios.get(
            "http://localhost:8000/api/get-edit-records"
        );
        this.tableData = response.data;
        console.log(this.tableData);
      } catch (error) {
        console.error('Error fetching edit records:', error);
      }
    },
    async fetchVersionData() {
      try {
        const response = await axios.get("http://localhost:8000/api/get-versions");
        this.versionData = response.data;
      } catch (error) {
        console.error('Error fetching version data:', error);
      }
    },
    async rollbackVersion(version) {
      try {
        await axios.post("http://localhost:8000/api/rollback", {version: version});
      } catch (error) {
        console.error('Error during rollback:', error);
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

/* Style for the button container */
.operation-buttons {
  display: flex;
  flex-direction: column;
  /* Stack buttons vertically */
  align-items: flex-start;
  /* Align buttons to the start of the flex container */
}

/* Style for individual buttons */
.operation-button {
  margin-bottom: 8px;
  /* Add bottom margin to each button except the last one */
}

.operation-button:last-child {
  margin-bottom: 0;
  /* Remove bottom margin from the last button */
}

.el-button + .el-button {
  margin-left: 0px;
}
</style>
