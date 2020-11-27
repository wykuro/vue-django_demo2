<template>
  <div class="dweb">
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>{{ page_name }}</el-breadcrumb-item>
    </el-breadcrumb>
  </div>
</template>
<script>
export default {
  props: ["page_name"],
};
</script>
<style scoped>
.dweb {
  padding: 20px 10px;
}
</style>