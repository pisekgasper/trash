<template>
  <div id="home">
    <div class="map-container">
      <slovenian-map v-if="!hide" />
    </div>
  </div>
</template>

<script>
import SlovenianMap from "../components/SlovenianMap.vue";

export default {
  data() {
    return {
      hide: true,
    };
  },
  components: {
    SlovenianMap,
  },
};
</script>

<style lang="scss" scoped>
#home {
  margin: 0;
  width: 100%;
  height: 100%;
}
.map-container {
  position: relative;
  width: 100%;
  height: 100%;
}
</style>
