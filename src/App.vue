<template>
  <!--<div id="nav">
		<router-link to="/">Home</router-link>
		<router-link to="/about">About</router-link>
	</div> 
	<router-view />-->
  <div id="content">
    <aside class="sidebar">
      <div class="theme-switcher-container">
        <theme-switcher></theme-switcher>
      </div>
    </aside>
    <main class="main">
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
    </main>
  </div>
</template>

<script>
import SlovenianMap from "./components/SlovenianMap.vue";
import ThemeSwitcher from "./components/ThemeSwitch.vue";
import MonthlyChart from "./components/MonthlyChart.vue";
import PieChart from "./components/PieChart.vue";
import http from "./http-common";

export default {
  data() {
    return {
      dashGrid: null,
      datacollection: null,
      state: null,
      state2: null,
      bgColor: "white",
    };
  },
  components: {
    ThemeSwitcher,
    SlovenianMap,
    MonthlyChart,
    PieChart,
  },
  mounted() {
    document.documentElement.classList.add("show-cursor");
    document.documentElement.setAttribute("data-theme", "dark");
    this.bgColor = getComputedStyle(document.documentElement).getPropertyValue(
      "--bg-05"
    );
    this.accentColor = getComputedStyle(
      document.documentElement
    ).getPropertyValue("--accent");
    this.dashGrid = document.querySelector(".main");
    this.expandedGraph = this.dashGrid.querySelector("#expanded-graph");
    this.showExpanded = false;
    this.fillData();
    this.fillData2();
  },
  methods: {
    fillData() {
      var x =
        "SELECT sum(kol_kg) AS teza FROM evl WHERE DATE_PART('year',dat_oddaje) = '2021' GROUP BY DATE_PART('month',dat_oddaje) LIMIT 8;";
      http
        .get("/trash", { params: { q: x } })
        .then((response) => {
          var arr = [];
          response.data.forEach((e) => {
            arr.push(Number(e.teza) / 1000000);
          });
          this.state = {
            chartData: {
              datasets: [
                {
                  data: arr,
                  backgroundColor: this.bgColor,
                  fill: false,
                  borderColor: this.accentColor,
                  tension: 0.1,
                },
              ],
              // These labels appear in the legend and in the tooltips when hovering different arcs
              labels: ["Jan", "Feb", "Mar", "Apr", "Maj", "Jun", "Jul", "Avg"],
            },
            chartOptions: {
              responsive: true,
              legend: {
                display: false,
              },
              tooltips: {
                callbacks: {
                  label: function (tooltipItem) {
                    return tooltipItem.yLabel;
                  },
                },
              },
            },
          };
          // this.datacollection = arr;
          // console.log(arr);
          console.log(this.state.chartData);
        })
        .catch((e) => {
          console.log(e);
          this.loading = false;
        });
    },
    fillData2() {
      var arr = [];
      var labs = [];
      var x =
        "select wol_num, count(wol_num) as st from evl group by wol_num ORDER BY st desc limit 5;";
      http
        .get("/trash", { params: { q: x } })
        .then((response) => {
          response.data.forEach((e) => {
            arr.push(Number(e.st));
            labs.push(e.wol_num);
          });
          arr.push(
            383399 -
              arr.reduce(function (a, b) {
                return a + b;
              }, 0)
          );
          labs.push("Ostalo");
          this.state2 = {
            chartData: {
              datasets: [
                {
                  data: arr,
                  backgroundColor: [
                    "red",
                    "blue",
                    "green",
                    "yellow",
                    "gray",
                    this.bgColor,
                  ],
                },
              ],
              // These labels appear in the legend and in the tooltips when hovering different arcs
              labels: labs,
            },
            chartOptions: {
              responsive: true,
              legend: {
                display: true,
              },
              hoverOffset: 4,
            },
          };
          // this.datacollection = arr;
          // console.log(arr);
          console.log(this.state.chartData);
        })
        .catch((e) => {
          console.log(e);
          this.loading = false;
        });
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
  top: 40px;
  transform: translateX(-50%);
  height: min-content;
}

.sidebar {
  grid-area: sidebar;
  position: relative;
  background-color: var(--bg-00);
}
.main {
  position: relative;
  background-color: transparent;
  max-height: 100vh;
  margin: 20px;
  display: flex;
  flex-flow: column nowrap;
  gap: 20px;
  justify-content: space-between;
}
.main .row {
  display: flex;
  flex-flow: row nowrap;
  gap: 20px;
}
.main .row:nth-child(1) {
  flex: 1;
}
.main .row:nth-child(2) {
  flex: 3;
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
</style>
