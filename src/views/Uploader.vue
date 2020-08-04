<template>
  <div class="form-groups">
    <h2>動画ファイルをアップロード</h2>
    <div class="form-group">
      <label for="title">タイトル</label>
      <input type="text" class="form-control" id="title" ref="title" placeholder="動画タイトル">
    </div>
    <div class="form-group">
      <label for="category">カテゴリー</label>
      <select class="form-control" id="category" ref="category">
        <option value=""></option>
        <option value="aws">AWS</option>
        <option value="orekike">このサービスは俺に聞け</option>
        <option value="twilio">Twilio</option>
      </select>
    </div>
    <div class="form-group">
      <label for="file">File</label>
      <input type="file" id="file" class="form-control-file" ref="file" v-on:change="handleFileUpload()"/>
    </div>
    <button v-on:click="submitFile()" class="btn btn-primary mb-2">Submit</button>
  </div>
</template>

<script>
  import axios from 'axios' 
  

  export default {
    data(){
      return {
        file: ''
      }
    },
    methods: {
      submitFile(){
        let formData = new FormData();
        let coolData = [this.$refs.title.value, this.$refs.category.value]
        formData.append('file', this.file);
        formData.append('cool_data', JSON.stringify( coolData ) );
        axios.post( this.$config.api_endpoint + '/video-upload',
          formData,
          {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
          }
        ).then(function(){
          console.log('upload success');
        })
        .catch(function(){
          console.log('upload failure');
        });
      },
      handleFileUpload(){
        this.file = this.$refs.file.files[0];
      }
    }
  }
</script>