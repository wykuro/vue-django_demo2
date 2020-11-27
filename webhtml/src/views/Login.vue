<template>
  <div id="login-page">
    <div class="dweb loginbox">
      <div class="header">
        用户登录
        <el-divider></el-divider>
      </div>
      <el-form
        :label-position="'right'"
        label-width="80px"
        :model="formData"
      >
        <el-form-item label="用户名">
          <el-input v-model="formData.username"></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="formData.password"></el-input>
        </el-form-item>
        <el-form-item>
            <el-button @click="Login()" type="success">登录</el-button>
            <el-button @click="toRegister()" type="success">前往注册</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      formData: {
        username: "",
        password: "",
      },
    }
  },
  methods:{
      Login(){
          if(this.formData.username.length==0||this.formData.password.length==0){
              alert('表单不完整')
              return
          }
          this.$store.dispatch('Login',this.formData)
      },
      toRegister(){
          this.$router.push({path:'/register'})
      }
  }
};
</script>
<style scoped>
#login-page {
  height: 80vh;
  display: flex;
  justify-content: center;
  align-items: center;
}
.loginbox {
  padding: 10px;
}
</style>