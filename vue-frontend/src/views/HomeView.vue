<template>
  <div>
    <el-container>
      <!--    SideBar  -->
      <el-aside :width="asideWidth" style="min-height: 100vh; background-color: #001529">
        <div style="height: 60px; color: white; display: flex; align-items: center; justify-content: center">
          <img src="@/assets/UCS-Logo.png" alt="" style="width: 120px; height: 60px">
        </div>

        <el-menu :collapse="isCollapse" :collapse-transition="false" router background-color="#001529" text-color="rgba(255, 255, 255, 0.65)" active-text-color="#fff" style="border: none" :default-active="$route.path">
          <el-menu-item index="/">
            <i class="el-icon-menu"></i>
            <span slot="title">Home Page</span>
          </el-menu-item>
          <el-menu-item index="/1">
            <i class="el-icon-house"></i>
            <span slot="title">Page 1</span>
          </el-menu-item>
          <el-menu-item index="/2">
            <i class="el-icon-house"></i>
            <span slot="title">Page 2</span>
          </el-menu-item>
          <el-submenu index="3">
            <template slot="title">
              <i class="el-icon-menu"></i>
              <span>Table Tools</span>
            </template>
            <el-menu-item>Table 1</el-menu-item>
            <el-menu-item>Table 2</el-menu-item>
            <el-menu-item index="/">Test</el-menu-item>
          </el-submenu>
        </el-menu>

      </el-aside>

      <el-container>
        <!--        Header-->
        <el-header>

<!--          <i :class="collapseIcon" style="font-size: 26px" @click="handleCollapse"></i>-->
          <el-breadcrumb separator-class="el-icon-arrow-right" style="margin-left: 20px">
            <el-breadcrumb-item :to="{ path: '/' }">Home Page</el-breadcrumb-item>
            <el-breadcrumb-item :to="{ path: '/user' }">Test</el-breadcrumb-item>
          </el-breadcrumb>

        </el-header>

        <!--        Main Page-->
        <el-main>
          <div style="box-shadow: 0 0 10px rgba(0,0,0,.1); padding: 10px 20px; border-radius: 5px; margin-bottom: 10px">
            This is UCS Team 2 Skynet
          </div>
          <el-card style="width: 500px">
            <div slot="header" class="clearfix">
              <span>Hello World</span>
            </div>
            <div>
              Mid-Term Demo
              <div style="margin-top: 20px">
                <div style="margin: 10px 0"><strong>Rating</strong></div>
                <el-button type="primary">5</el-button>
                <el-button type="success">4</el-button>
                <el-button type="warning">3</el-button>
                <el-button type="danger">2</el-button>
                <el-button type="info">1</el-button>
              </div>
            </div>
          </el-card>
        </el-main>

      </el-container>


    </el-container>
  </div>
</template>

<script>

export default {
  name: 'HomeView',
  data() {
    return {
      isCollapse: false,
      asideWidth: '200px',
      collapseIcon: 'el-icon-s-fold'
    }
  }
  // Systolic Function
  //
  // methods: {
  //   handleFull() {
  //     document.documentElement.requestFullscreen()
  //   },
  //   handleCollapse() {
  //     this.isCollapse = !this.isCollapse
  //     this.asideWidth = this.isCollapse ? '64px' : '200px'
  //     this.collapseIcon = this.isCollapse ? 'el-icon-s-unfold' : 'el-icon-s-fold'
  //   }
  // }
}
</script>

<style>
.el-menu--inline {
  background-color: #000c17 !important;
}
.el-menu--inline .el-menu-item {
  background-color: #000c17 !important;
  padding-left: 49px !important;
}
.el-menu-item:hover, .el-submenu__title:hover {
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
.el-menu-item.is-active i, .el-menu-item.is-active .el-tooltip{
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
  box-shadow: 2px 0 6px rgba(0,21,41,.35);
}
.logo-title {
  margin-left: 5px;
  font-size: 20px;
  transition: all .3s;   /* 0.3s */
}
.el-header {
  box-shadow: 2px 0 6px rgba(0,21,41,.35);
  display: flex;
  align-items: center;
}
</style>