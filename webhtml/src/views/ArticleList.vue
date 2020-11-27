<template>
  <div id="article-list">
    <div class="dweb">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>文章列表</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="dweb" style="margin-top: 10px">
      <el-row>
        <el-col v-for="item in article_list" :key="item.id" :span="24">
          <div class="card dweb">
            <el-row>
              <el-col :xs="24" :lg="6">
                <el-image
                  v-if="screerWidth > 500"
                  style="width: 150px; height: 80px"
                  :src="item.cover"
                  :fit="'cover'"
                ></el-image>
                <el-image
                  v-else
                  style="width: 100%"
                  :src="item.cover"
                  :fit="'cover'"
                ></el-image>
              </el-col>
              <el-col class="text-item" :xs="24" :lg="4">
                <span id="ada">
                  {{ item.title }}
                </span>
              </el-col>
              <el-col class="text-item" :xs="12" :lg="7">
                <span> 发布者:{{ item.nickName }} </span>
              </el-col>
              <el-col class="text-item" :xs="12" :lg="7">
                <el-button
                  @click="toArticle(item.id)"
                  type="success"
                  icon="el-icon-search"
                  circle
                ></el-button>
                <el-button
                  type="danger"
                  icon="el-icon-delete"
                  circle
                  @click="deleteArticle(item.id)"
                ></el-button>
              </el-col>
            </el-row>
          </div>
        </el-col>
      </el-row>
    </div>
    <div class="dweb" style="margin-top: 10px">
      <el-pagination
        background
        layout="prev, pager, next"
        :total="total"
        :page-size="pagesize"
        @current-change="currentChange"
      >
      </el-pagination>
    </div>
  </div>
</template>
<script>
import axios from "axios";
import Qs from "qs";
export default {
  props: ["screerWidth"],
  data() {
    return {
      total: 100,
      pagesize: 3,
      currentpage: 1,
      article_list: [],
    };
  },
  mounted() {
    this.getListData(this.currentpage);
  },
  methods: {
    toArticle(id){
      this.$router.push({path:'/article',query:{id:id}})
    },
    currentChange(val) {
      console.log(val);
      this.currentpage = val;
      this.getListData(val);
    },
    getListData(page) {
      axios({
        url: "http://127.0.0.1:9000/api/article-list",
        method: "get",
        params: {
          page,
          pageSize: this.pagesize,
        },
      }).then((res) => {
        console.log(res);
        this.total = res.data.total;
        this.article_list = res.data.data;
      });
    },
    deleteArticle(id) {
      if (confirm("是否确定删除")) {
        let checkInfo = {
          contentType: "blog_article",
          permissions: ["delete"],
        };
        this.$store.dispatch("checkUserPerm", checkInfo).then((res) => {
          console.log(res);
          if (res) {
            axios({
              url: "http://127.0.0.1:9000/api/del-article",
              method: "delete",
              headers: {
                "Content-Type": "application/x-www-form-urlencoded",
              },
              data: Qs.stringify({
                id,
                token: this.$store.getters.isLogin,
              }),
            }).then((res) => {
              console.log(res);
              if (res.data == "nologin") {
                alert("用户信息错误");
                return;
              }
              this.getListData(this.currentpage);
            });
          }
        });
      }
    },
  },
};
</script>
<style scoped>
#article-list .dweb {
  padding: 20px 10px;
}
.card.dweb .text-item {
  color: #fff;
  height: 80px;
  display: flex;
  justify-content: center;
  align-items: center;
}
#ada {
  width: 80%;
}
</style>