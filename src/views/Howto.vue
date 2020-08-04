<template>
  <div v-if="$route.params.name === 'upload' ">
    <howto-upload />
  </div>
  <div v-else-if="$route.params.name === 'ofuse' ">
    <howto-ofuse />
  </div>
</template>

<script>
import HowtoUpload from "../components/HowtoUpload";
import HowtoOfuse from "../components/HowtoOfuse";

export default {
  name: "home",
  components: {
    HowtoUpload,
    HowtoOfuse
  }
};
</script>

<style lang="scss" scoped>
.next-steps {
  .fa-link {
    margin-right: 5px;
  }
}
</style>