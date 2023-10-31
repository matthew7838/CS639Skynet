<template>
  <div>
      <el-container>
          <!--    SideBar  -->
          <el-aside :width="asideWidth" style="min-height: 100vh; background-color: #001529">
              <div style="height: 60px; color: white; display: flex; align-items: center; justify-content: center">
                  <img src="@/assets/UCS-Logo.png" alt="" style="width: 120px; height: 60px">
              </div>

              <el-menu :collapse="isCollapse" :collapse-transition="false" router background-color="#001529"
                  text-color="rgba(255, 255, 255, 0.65)" active-text-color="#fff" style="border: none"
                  :default-active="$route.path">
                  <el-menu-item index="/">
                      <i class="el-icon-house"></i>
                      <span slot="title">Home Page</span>
                  </el-menu-item>
                  <el-menu-item index="/1">
                      <i class="el-icon-house"></i>
                      <span slot="title">New Scrape Data</span>
                  </el-menu-item>
                  <el-menu-item index="/1">
                      <i class="el-icon-house"></i>
                      <span slot="title">History</span>
                  </el-menu-item>
              </el-menu>

          </el-aside>

          <el-container>
              <!--        Header-->
              <el-header>

                  <!--          <i :class="collapseIcon" style="font-size: 26px" @click="handleCollapse"></i>-->
                  <el-breadcrumb separator-class="el-icon-arrow-right" style="margin-left: 20px">
                      <el-breadcrumb-item :to="{ path: '/' }">Home Page</el-breadcrumb-item>
                  </el-breadcrumb>

              </el-header>

              <!--        Main Page-->
              <el-main>
                  <el-table :data="tableData" style="width: 100%">
                      <el-table-column prop="JCAT" label="JCAT"></el-table-column>
                      <el-table-column prop="name" label="Name"></el-table-column>
                      <el-table-column prop="type" label="Type" :filters="typeFilters"
                          :filter-method="filterHandler"></el-table-column>
                      <el-table-column prop="piece" label="Piece"></el-table-column>
                      <el-table-column prop="PL_name" label="PL Name" width="120"></el-table-column>
                      <el-table-column prop="parent" label="Parent"></el-table-column>
                      <el-table-column prop="state" label="State"></el-table-column>
                      <el-table-column prop="owner" label="Owner" :filters="ownerFilters"
                          :filter-method="filterHandler"></el-table-column>
                      <el-table-column prop="manufacturer" label="Manufacturer" width="120"></el-table-column>
                      <el-table-column prop="bus" label="Bus"></el-table-column>
                      <el-table-column prop="status" label="Status" :filters="statusFilters"
                          :filter-method="filterHandler"></el-table-column>
                      <el-table-column prop="altname" label="Alternative Name" width="150"></el-table-column>
                      <el-table-column prop="dest" label="Destination" width="150"></el-table-column>
                  </el-table>

              </el-main>

          </el-container>


      </el-container>
  </div>
</template>

<script>

import axios from 'axios';
export default {
  data() {
      return {
          isCollapse: false,
          asideWidth: '200px',
          collapseIcon: 'el-icon-s-fold',
          tableData: []
      };
  },
  mounted() {
      this.fetchSatellites();
  },
  methods: {
      async fetchSatellites() {
          try {
              const response = await axios.get('http://localhost:8000/api/satellites'); // replace with your Flask app URL
              this.tableData = response.data;
          } catch (error) {
              console.error('There was an error fetching the data:', error);
          }
      }
  }
}


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
  transition: width .3s;
  box-shadow: 2px 0 6px rgba(0, 21, 41, .35);
}

.logo-title {
  margin-left: 5px;
  font-size: 20px;
  transition: all .3s;
  /* 0.3s */
}

.el-header {
  box-shadow: 2px 0 6px rgba(0, 21, 41, .35);
  display: flex;
  align-items: center;
}</style>