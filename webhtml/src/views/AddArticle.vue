<template>
  <div>
    <el-row :gutter="10">
      <el-col :xs="24" :lg="8">
        <div class="dweb">
          <el-form
            :label-position="'left'"
            label-width="80px"
            :model="article_info"
          >
            <el-form-item label="文章标题">
              <el-input v-model="article_info.title"></el-input>
            </el-form-item>
            <el-form-item label="文章描述">
              <el-input type="textarea" :rows="4" v-model="article_info.describe"></el-input>
            </el-form-item>
          </el-form>
        </div>
      </el-col>
      <el-col :xs="24" :lg="16">
        <div class="dweb">
          <div v-for="(img,index) in cover_list" :key="index">
            <el-image
            v-if="img==cover_img"
            class="cover"
            style="width:150px;height:150px"
            :src='img'
            :fit="'cover'"
            @click="chooseCover(img)"
            ></el-image>
            <el-image
            v-else
            class=""
            style="width:150px;height:150px"
            :src='img'
            :fit="'cover'"
            @click="chooseCover(img)"
            ></el-image>
          </div>
          <el-button @click="submitArticle" type="success" round>保存</el-button>
        </div>
      </el-col>
      <el-col :xs="24" :lg="24">
        <div class="dweb">
            <div id="summernote">summernote</div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import $ from 'jquery'
import axios from 'axios';
import Qs from 'qs';
export default {
    data(){
        return{
            article_info:{
                title:"",
                describe:"",
                contents:""
            },
            cover_img:"",
            cover_list:[]
        }
    },
    mounted(){
        this.summernote()
    },
    methods: {
        summernote(){
          let self=this
            $('#summernote').summernote({
                width:'100%',
                height:300,
                lang:'zh-CN',
                callbacks:{
                  onChange(contents){
                    self.article_info.contents=contents
                  },
                  onImageUpload(files){
                    // console.log(files)
                    let img=files[0]
                    let imgData=new FileReader()
                    imgData.readAsDataURL(img)
                    // console.log(imgData)
                    imgData.onload=function(){
                      // console.log(imgData.result);
                      let imgnode=document.createElement('img')
                      imgnode.src=imgData.result
                      $("#summernote").summernote('insertNode',imgnode)
                      self.cover_list.push(imgData.result)
                    }
                  },
                  onImageLinkInsert(url){
                    // console.log(url);
                    let imgnode=document.createElement('img')
                    imgnode.src=url
                    // console.log(imgnode);
                    $("#summernote").summernote('insertNode',imgnode)
                    self.cover_list.push(url)
                  },
                  onMediaDelete(target){
                    let imgData=target[0].src
                    console.log(imgData);
                    for(let i=0;i<self.cover_list.length;i++){
                      if(self.cover_list[i]==imgData){
                        self.cover_list.splice(i,1)
                      }
                    }
                  }
                }
            });
        },
        chooseCover(img){
          this.cover_img=img
        },
        submitArticle(){
          let article_data={
            title:this.article_info.title,
            describe:this.article_info.describe,
            content:this.article_info.contents,
            cover:this.cover_img,
            token:this.$store.getters.isLogin
          }
          axios.post(
          'http://127.0.0.1:9000/api/add-article/',
          Qs.stringify(article_data) 
          )
          .then(res => {
            if(res.data=='notitle'){
              alert('标题为空')
              return
            }
            if(res.data=='nologin'){
              alert('用户信息错误')
              return
            }
            if(res.data=='ok'){
              window.location.reload()
            }
          })
          .catch(e => {
            console.log(e);
          })
        },
    },
};
</script>
<style scoped>
.dweb {
  min-height: 200px;
  padding: 20px 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.el-form-item{
    margin-top: 22px;
}
.dweb .el-button{
  position: fixed;
  right: 20px;
  margin-top: 130px;
  z-index: 1001;
}
.dweb .el-image:hover{
  border: 3px solid rgb(245, 230, 25);
}
.dweb .el-image.cover{
  border: 3px solid rgb(245, 230, 25);
}
</style>