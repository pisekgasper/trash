<template>
  <div class="switch-wrapper">
    <span>Light</span>
    <label id="switch"
      ><input type="checkbox" v-model="checked" v-on:change="toggle" />
      <div></div>
    </label>
    <span>Dark</span>
  </div>
</template>

<script>
import * as d3 from "d3";

export default {
  data() {
    return {
      checked: true,
    };
  },
  methods: {
    toggle() {
      const html = document.documentElement;
      if (this.checked) html.setAttribute("data-theme", "dark");
      else html.setAttribute("data-theme", "light");

      const accentColor = getComputedStyle(
        document.documentElement
      ).getPropertyValue("--accent");
      const svg = d3.select("#map-svg");
      svg.select(".regions").selectAll("path").attr("fill", "transparent");
      svg.select(".regional-borders").attr("stroke", accentColor);
    },
  },
};
</script>

<style lang="scss" scoped>
#switch input {
  position: absolute;
  opacity: 0;
}

#switch {
  display: inline-block;
  font-size: 15px; /* 1 */
  height: 1em;
  width: 2em;
  background: var(--bg-03);
  border-radius: 1em;
  vertical-align: middle;
}

#switch div {
  height: 1em;
  width: 1em;
  border-radius: 1em;
  background: var(--accent);
  box-shadow: 0 0.1em 0.3em rgba(0, 0, 0, 0.3);
  transform: scale(1.1);
  -webkit-transition: all 100ms ease-out;
  -moz-transition: all 100ms ease-out;
  transition: all 100ms ease-out;
}

#switch input:checked + div {
  background-color: var(--accent);
  -webkit-transform: translate3d(100%, 0, 0) scale(1.1);
  -moz-transform: translate3d(100%, 0, 0) scale(1.1);
  transform: translate3d(100%, 0, 0) scale(1.1);
}

.switch-wrapper {
  line-height: 20px;
  white-space: nowrap;
}

.switch-wrapper span {
  padding: 0 10px;
  font-size: 11px;
  color: var(--font-disabled);
}
</style>