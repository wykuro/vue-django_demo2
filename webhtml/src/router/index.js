import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '../store'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    beforeEnter: (to, from, next) => {
      if(store.state.userinfo.token){
        next()
      }
      else{
        next('/login')
      }
    }
  },
  {
    path: '/add-article',
    name: 'AddArticle',
    component: () => import('../views/AddArticle.vue'),
    beforeEnter: (to, from, next) => {
      if(store.state.userinfo.token){
        next()
      }
      else{
        next('/login')
      }
    }
  },
  {
    path: '/article-list',
    name: 'ArticleList',
    component: () => import('../views/ArticleList.vue'),
    beforeEnter: (to, from, next) => {
      if(store.state.userinfo.token){
        next()
      }
      else{
        next('/login')
      }
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue')
  },
  {
    path: '/user-perm',
    name: 'UserPerm',
    component: () => import('../views/UserPerm.vue'),
    beforeEnter: (to, from, next) => {
      if(store.state.userinfo.token){
        let checkInfo={
          contentType:'auth_user',
          permissions:['add','change','delete','view']
        }
        store.dispatch('checkUserPerm', checkInfo).then((res)=>{
          if(res){
            next()
          }
        })
      }
      else{
        next('/login')
      }
    }
  },
  {
    path: '/article',
    name: 'Article',
    component: () => import('../views/Article.vue'),
    beforeEnter: (to, from, next) => {
      if(store.state.userinfo.token){
        let checkInfo={
          contentType:'blog_articl',
          permissions:['view']
        }
        store.dispatch('checkUserPerm', checkInfo).then((res)=>{
          if(res){
            next()
          }
        })
      }
      else{
        next('/login')
      }
    }
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },

]
const routerPush=VueRouter.prototype.push
VueRouter.prototype.push=function push(location){
  return routerPush.call(this,location).catch(err=>err)
}
const router = new VueRouter({
  routes
})
export default router
