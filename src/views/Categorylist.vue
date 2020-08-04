<template>
  <div id="category" class="row">
    <div v-show="loadings" class="loader">Now loading...</div>

    <div class="col-sm-6 col-md-3" v-for="(value, key) in source" :key="key">
      <p><a href="/archives">全ての動画はここ</a></p>
      <div class="card img-thumbnail h-100">
        <a v-bind:href="'/view/'+value.contentsId"><img class="card-img-top" v-bind:src="value.thumbnailUrl | replace('{params}', 'so_1,w_245')" alt="カードの画像"></a>
        <div class="card-body px-2 py-3">
          <h5 class="card-title"><a v-bind:href="'/view/'+value.contentsId">{{ value.title }}</a></h5>
          <a v-bind:href="'/categorylist/'+ value.categorySlug" class="btn btn-secondary btn-sm">{{ value.category }}</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  export default {
    name: "app",
    data: function(){
      return {source: null,loadings: true,}
    },
    mounted: function() {
      axios
        .get(this.$config.api_endpoint + '/cat/' + this.$route.params['slug'])
        .then(response => {
          this.source = response.data.data
        })
        .catch(error => console.log(error))
        .finally(() => this.loadings = false)
    },
    filters: {
      replace:function(val){
          console.log(val);
          return val.replace("{params}", "so_1,w_245");   
      }
    },
  };
</script>