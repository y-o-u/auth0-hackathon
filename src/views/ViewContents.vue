<template>
  <div v-if="exist" id="player">
    <!--<img alt="Vue logo" src="./assets/logo.png" />-->
    <div v-show="loading" class="loader">Now loading...</div>
    <Player :source="source" v-if="source" />
  </div>
  <div v-else>
    お探しのページは見つかりませんでした
  </div>
</template>

<script>
  import Player from "../components/Player.vue";
  import axios from 'axios'

  export default {
    name: "app",
    components: {
      Player
    },
    data: function(){
      return {source: null,loading: true, exist: true}
    },
    mounted: function() {
      axios
        .get(this.$config.api_endpoint + '/contents/' + this.$route.params['id'])
        .then(response => {
          this.source = response.data.data
        })
        .catch(error => {
          console.log(error)
          this.exist = false
        })
        .finally(() => this.loading = false)
    }
  };
</script>
