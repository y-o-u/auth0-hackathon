<template>
  <div id="content" class="container">
    <div
      class="theoplayer-container video-js theoplayer-skin vjs-16-9 THEOplayer"
      ref="theoplayer"
    >
    </div>

    <article>
      <h2>{{ source.title }}</h2>
      <a href="" class="btn btn-secondary btn-sm">{{ source.category }}</a>
    </article>

    <pre class="rounded w-100">
      <code class="json hljs">{{ source }}</code>
    </pre>
  </div>
</template>

<script>
  export default {
    props: ["source"],
    mounted: function() {
      this.playerInit();
    },
    methods: {
      playerInit() {
        const player = new window.THEOplayer.Player(this.$refs.theoplayer, {
          fluid: true,
          libraryLocation: "https://cdn.myth.theoplayer.com/7c395c1d-bedf-4b89-a064-81d88566eb8b",
          pip: {
              "visibility": 0.7
          }
        });
        player.source = {
          sources: [{
            //"src": this.source.url,//this.source.url.replace("{params}", "c_scale,f_auto"),
            //"type": this.source.type
            src : 'https://cm-pa-contents.s3-ap-northeast-1.amazonaws.com/blog/dash/BigBuckBunny_1080.mpd', // sets DASH source
            type : 'application/dash+xml' // sets type to MPEG-DASH
          },{
            src : 'https://cm-pa-contents.s3-ap-northeast-1.amazonaws.com/blog/BigBuckBunny_1080.mp4', // sets DASH source
            type : 'video/mp4' // sets type to MPEG-DASH
          }]
          /*ads: [{
            sources: "https://res.cloudinary.com/classmethod-japan/raw/upload/v1593185722/study-archives/ads/vmap/yqaiz0xq4uvlyiegyjba.xml",
            "timeOffset": "start",
            "skipOffset": 2
          }]*/
        };
        
      }
    }
  };
</script>
<style>
  .THEOplayer {
    max-width: var(--ytd-watch-flexy-max-player-width);
    min-width: var(--ytd-watch-flexy-min-player-width);
    margin: 0 auto;
  }

</style>
