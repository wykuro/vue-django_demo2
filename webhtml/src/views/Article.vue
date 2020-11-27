<template>
  <div>
    <BreadMenu :page_name="article_data.title"></BreadMenu>
    <el-row :gutter="10">
      <el-col :xs="24" :lg="16">
        <div class="dweb">
          {{ article_data.title }}
        </div>
        <div class="dweb">
          {{ article_data.describe }}
        </div>
        <div class="dweb">
          <div v-html="article_data.content"></div>
          <div class="clear"></div>
        </div>
        <div class="dweb">
          <el-button-group>
            <el-button
              v-if="article_data.pre_id == 0"
              type="info"
              icon="el-icon-arrow-left"
              disabled
              >没有了</el-button
            >
            <el-button
              v-else
              type="primary"
              icon="el-icon-arrow-left"
              @click="toOtherPage(article_data.pre_id)"
              >上一页</el-button
            >
            <el-button v-if="article_data.next_id == 0" type="info" disabled
              >没有了<i class="el-icon-arrow-right el-icon--right"></i
            ></el-button>
            <el-button
              v-else
              type="primary"
              @click="toOtherPage(article_data.next_id)"
              >下一页<i class="el-icon-arrow-right el-icon--right"></i
            ></el-button>
          </el-button-group>
        </div>
      </el-col>
      <el-col :xs="24" :lg="8">
        <div class="dweb">
          <el-image
            style="width: 100px; height: 100px"
            :src="article_data.cover"
            :fit="'cover'"
          ></el-image>
        </div>
        <div class="dweb">
          admin：
          <el-divider></el-divider>
          hhhhh
        </div>
        <div class="dweb">
          <el-input
            type="textarea"
            :autosize="{ minRows: 2, maxRows: 4 }"
            placeholder="请输入内容"
            v-model="new_pinglun"
          >
          </el-input>
        </div>
      </el-col>
    </el-row>
  </div>
</template>
<script>
import BreadMenu from "../components/BreadMenu";
import axios from "axios";
export default {
  data() {
    return {
      article_id: this.$route.query.id,
      article_data: {},
      new_pinglun:""
    };
  },
  components: {
    BreadMenu,
  },
  mounted() {
    this.getArticleData(this.article_id);
  },
  watch: {
    $route(to) {
      this.getArticleData(to.query.id);
    },
  },
  methods: {
    getArticleData(id) {
      console.log(id);
      axios({
        url: "http://127.0.0.1:9000/api/article-data/",
        method: "get",
        params: {
          id,
        },
      }).then((res) => {
        this.article_data = res.data;
      });
    },
    toOtherPage(id) {
      if (id == 0) {
        alert("没有了");
      }
      this.$router.push({ path: "/article", query: { id: id } });
    },
  },
};
</script>
<style scoped>
.dweb {
  margin-top: 10px;
  padding: 10px;
}
</style>