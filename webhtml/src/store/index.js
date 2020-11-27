import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import Qs from 'qs'
import router from '../router'
Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    userinfo:{}
  },
  getters:{
    isLogin(state){
      return state.userinfo.token
    }
  },
  mutations: {
    saveUserinfo(state,userinfo){
      state.userinfo=userinfo
    },
    clearUserinfo(state){
      state.userinfo={}
    }
  },
  actions: {
    //登录
    Login({commit},formData){
      axios({
        url:"http://127.0.0.1:9000/api/dweb-login/",
        method:'post',
        data:Qs.stringify(formData)
    }).then((res)=>{
        if(res.data=='none'){
            alert('用户名不存在')
            return
        }
        if(res.data=='pwderr'){
            alert('密码错误')
            return
        }
        commit('saveUserinfo',res.data)
        localStorage.setItem('token',res.data.token)
        router.push({path:'/'})
    })
    },
    //注册
    Register({commit},formData){
      axios({
        url:'http://127.0.0.1:9000/api/dweb-register/',
        method:"post",
        data:Qs.stringify(formData)
    }).then((res)=>{
        if(res.data=='repeat'){
            alert("用户名存在")
            return
        }
        commit('saveUserinfo',res.data)
        router.push({path:'/login'})
    })
    },
    Logout({commit},token){
      commit('clearUserinfo')
      localStorage.removeItem('token')
      axios({
        url:"http://127.0.0.1:9000/api/dweb-logout/",
        method:"post",
        data:Qs.stringify({token})
      }).then((res)=>{
        console.log(res);
      })
    },
    autoLogin({commit}){
      let token=localStorage.getItem('token')
      if(token){
        axios({
          url:"http://127.0.0.1:9000/api/auto-login/",
          method:"post",
          data:Qs.stringify({token})
        }).then((res)=>{
          commit('saveUserinfo',res.data)
          localStorage.setItem('token',res.data.token)
          router.push({path:'/'})
        })
      }
    },
    async checkUserPerm({getters},checkInfo){
      let token=getters.isLogin
      let contentType=checkInfo.contentType
      let permissions=checkInfo.permissions
      let perm_data;
      await axios({
        url:"http://127.0.0.1:9000/api/dweb-checkperm/",
        method:"post",
        data:Qs.stringify({
          token,
          contentType,
          permissions:JSON.stringify(permissions)
        })
      }).then((res)=>{
        if(res.data=='nologin'){
          perm_data=false
          alert('用户信息错误')
          return
        }
        if(res.data=='noperm'){
          perm_data=false
          alert("权限不足")
          return
        }
        if(res.data=='ok'){
          perm_data=true
        }
      })
      return perm_data
    }
  },
  modules: {
  }
})
