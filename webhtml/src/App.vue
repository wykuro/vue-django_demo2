<template>
  <div id="app">
    <div id="top-menu" class="dweb"></div>
    <div id="left-menu" :class="'dweb ' + mobile_left">
      <i @click="showHideLeftMenu" id="left-btn" class="el-icon-s-grid"></i>
      <el-col :span="24" style="margin-top:80px">
        <el-menu
          class="el-menu-vertical-demo"
          background-color="#00000000"
          text-color="#fff"
          active-text-color="#ffc815"
          @select="chooseMenu"
        >
          <el-submenu index="1">
            <template slot="title">
              <i class="el-icon-folder"></i>
              <span>文章管理</span>
            </template>
            <el-menu-item-group>
              <el-menu-item index="/add-article">发布文章</el-menu-item>
              <el-menu-item index="/article-list">文章列表</el-menu-item>
            </el-menu-item-group>
          </el-submenu>
          <el-menu-item index="/user-perm">
            <i class="el-icon-user"></i>
            <span slot="title">用户管理</span>
          </el-menu-item>
          <el-menu-item index="3">
            <i class="el-icon-s-operation"></i>
            <span slot="title">打赏记录</span>
          </el-menu-item>
          <el-menu-item index="4">
            <i class="el-icon-s-operation"></i>
            <span slot="title">栏目管理</span>
          </el-menu-item>
          <el-menu-item v-if="authUserLogin" @click="Logout()">
            <i class="el-icon-back"></i>
            <span slot="title">退出登录</span>
          </el-menu-item>
        </el-menu>
      </el-col>
    </div>
    <div id="content" :class="mobile_content">
      <router-view :screerWidth="screerWidth"></router-view>
      <div id="footer" class="dweb">
        <span>wykuro</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      screerWidth: document.body.clientWidth,
      mobile_left: "",
      mobile_content: "",
    };
  },
  computed:{
    authUserLogin(){
      return this.$store.getters.isLogin
    }
  },
  watch:{
    authUserLogin(newVal){
      if(newVal==null){
        this.$router.push({path:'/login'})
      }
    }
  },
  created(){
    this.$store.dispatch('autoLogin')
  },
  mounted() {
    this.changeDevice();
  },
  methods: {
    changeDevice() {
      if (this.screerWidth <= 500) {
        this.mobile_left = "xs";
        this.mobile_content = "xs";
      }
    },
    showHideLeftMenu() {
      if (this.mobile_left == "") {
        this.mobile_left = "xs";
      } else {
        this.mobile_left = "";
      }
      if (this.screerWidth > 500) {
        if (this.mobile_content == "") {
          this.mobile_content = "xs";
        } else {
          this.mobile_content = "";
        }
      }
    },
    chooseMenu(index){
      this.$router.push({path:index})
    },
    Logout(){
      this.$store.dispatch('Logout',this.$store.getters.isLogin)
    },
  },
};
</script>

<style>
.el-col {
  margin-top: 10px;
}
</style>
