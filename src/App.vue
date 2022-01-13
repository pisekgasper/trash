<template>
  <div id="content">
    <custom-cursor></custom-cursor>
    <aside class="sidebar">
      <div class="theme-switcher-container">
        <div class="switch-wrapper">
          <span>Light</span>
          <label id="switch"
            ><input type="checkbox" v-model="darkTheme" v-on:change="toggle" />
            <div></div>
          </label>
          <span>Dark</span>
        </div>
      </div>
      <img class="fri-logo" v-if="darkTheme" src="@/assets/fri_logo.png" />
      <img
        class="fri-logo"
        v-if="!darkTheme"
        src="@/assets/fri_logo_black.png"
      />
      <ul id="Menu">
        <li
          v-bind:class="{ selectedtab: selectedTab == 0 }"
          v-on:click="selectTab(0)"
        >
          Zemljevid Slovenije
        </li>
        <li
          v-bind:class="{ selectedtab: selectedTab == 1 }"
          v-on:click="selectTab(1)"
        >
          Vrste odpadkov
        </li>
        <li
          v-bind:class="{ selectedtab: selectedTab == 2 }"
          v-on:click="selectTab(2)"
        >
          Mikroiskanje
        </li>
        <li
          v-bind:class="{ selectedtab: selectedTab == 3 }"
          v-on:click="selectTab(3)"
        >
          Statistika
        </li>
      </ul>
    </aside>
    <main class="main">
      <div class="container">
        <keep-alive
          ><slovenian-map v-if="selectedTab == 0"></slovenian-map
        ></keep-alive>
        <keep-alive
          ><trash-type v-if="selectedTab == 1" ref="trashTypes"></trash-type
        ></keep-alive>
        <keep-alive
          ><personal-number v-if="selectedTab == 2"></personal-number
        ></keep-alive>
        <keep-alive>
          <statistics v-if="selectedTab == 3"></statistics>
        </keep-alive>
      </div>
    </main>
  </div>
</template>

<script>
import SlovenianMap from "./components/SlovenianMap.vue";
import CustomCursor from "./components/CustomCursor.vue";
import TrashType from "./components/TrashType.vue";
import PersonalNumber from "./components/PersonalNumber.vue";
import Statistics from "./components/Statistics.vue";
// import * as d3 from "d3";

export default {
  data() {
    return {
      selectedTab: 0,
      darkTheme: true,
    };
  },
  components: {
    SlovenianMap,
    CustomCursor,
    TrashType,
    PersonalNumber,
    Statistics,
  },
  mounted() {
    document.documentElement.classList.add("show-cursor");
    document.documentElement.setAttribute("data-theme", "dark");
  },
  methods: {
    selectTab(i) {
      this.selectedTab = i;
    },
    toggle() {
      const html = document.documentElement;
      if (this.darkTheme) html.setAttribute("data-theme", "dark");
      else html.setAttribute("data-theme", "light");

      // const accentColor = getComputedStyle(
      //   document.documentElement
      // ).getPropertyValue("--accent");
      // const svg = d3.select("#map-svg");

      // svg.select(".regions").selectAll("path").attr("fill", "transparent");
      // svg.select(".regional-borders").attr("stroke", accentColor);
    },
  },
};
</script>

<style lang="scss">
@import "./assets/css/reset.css";
@import "./assets/css/global.css";

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: var(--font-color);

    &.router-link-exact-active {
      color: var(--primary-color);
    }
  }
}

#content {
  margin: 0 !important;
  position: relative;
  height: 100vh;
  background-color: transparent;
  //overflow: hidden;
  max-height: 100vh;
  display: grid;
  grid-template-areas: "sidebar main";
  grid-template-columns: minmax(200px, 25%) 1fr;
  grid-template-rows: 1fr;
}

.theme-switcher-container {
  position: absolute;
  left: 50%;
  bottom: 40px;
  transform: translateX(-50%);
  height: min-content;
}

.sidebar {
  grid-area: sidebar;
  position: relative;
  background-color: var(--bg-01);
}
.main {
  grid-area: main;
  position: relative;
  background-color: transparent;
  max-height: 100vh;
  margin: 40px;
}

.main .container {
  position: absolute;
  width: 100%;
  height: min-content;
  padding: 3vh 4vh;
  top: 50%;
  transform: translateY(-50%);
  max-height: 100%;
  background-color: var(--bg-02);
  border-radius: 4vh;
}

.graph-container {
  flex: 1;
  overflow: hidden;
  position: relative;
  background-color: var(--bg-02);
  display: flex;
  flex-direction: column;
  flex-wrap: nowrap;
  border-radius: 15px;
}
.graph-container .heading {
  width: 100%;
  text-decoration: uppercase;
  pointer-events: none;
  position: relative;
}
.graph-container .heading div:nth-child(1) {
  width: max-content;
  margin: 20px 40px;
  font-weight: bold;
  pointer-events: none;
}
.graph-container .graph-content {
  flex-grow: 1;
  max-height: 100%;
  max-width: 100%;
  overflow: hidden;
  text-align: center;
  padding: 0px 20px 20px 20px;
}
#Menu {
  position: relative;
  margin-top: 5vh;
  width: 100%;
  height: min-content;
  text-align: right;
}
#Menu li {
  float: right;
  border-radius: 7vh 0 0 7vh;
  height: 4em;
  line-height: 4em;
  padding-right: 2em;
  padding-left: 2em;
  margin: 1rem 0;
  width: min-content;
  white-space: nowrap;
  font-size: 1.3em;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  cursor: pointer;
  font-weight: 400;
}
#Menu li:not(.selectedtab):hover {
  background-color: var(--bg-02);
}

.selectedtab {
  background-color: var(--bg-00);
  transition: all 0.8s cubic-bezier(0.31, 0.68, 0.17, 0.95);
}

.fri-logo {
  height: 25vh;
  margin: auto;
}
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
 
 <!-- 
<div class="row">
        <div class="graph-container shadow-02">
          <div class="heading">
            <div>GRAPH 1</div>
          </div>
          <div class="graph-content"></div>
        </div>
        <div class="graph-container shadow-02" @click="expand">
          <div class="heading">
            <div>TIP ODPADKOV POGOSTOST</div>
            <pie-chart
              v-if="state2"
              v-bind:chartData="state2.chartData"
              v-bind:chartOptions="state2.chartOptions"
			  style="margin: 20px"
            ></pie-chart>
          </div>
          <div class="graph-content" @click="expand"></div>
        </div>
        <div class="graph-container shadow-02" @click="expand">
          <div class="heading">
            <div>ODDAJA PO MESECIH</div>
          </div>
          <div class="graph-content">
            <monthly-chart
              v-if="state"
              v-bind:chartData="state.chartData"
              v-bind:chartOptions="state.chartOptions"
            ></monthly-chart>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="graph-container shadow-02" @click="expand" style="flex: 1">
          <div class="heading">
            <div>DATA 4</div>
          </div>
          <div class="graph-content"></div>
        </div>
        <div
          id="regions-map"
          class="graph-container shadow-02"
          @click="expand"
          style="flex: 2"
        >
          <div class="heading">
            <div>ZEMLJEVID OBČIN</div>
          </div>
          <div class="graph-content">
            <slovenian-map></slovenian-map>
          </div>
        </div>
      </div> 
-->