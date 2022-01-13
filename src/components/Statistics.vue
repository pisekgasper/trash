<template>
  <div class="four_charts">
    <div class="chart1">
      <h1>KOLIČINA ODPADKOV PO LETIH</h1>
      <column-chart
        ytitle="Teža v Mt"
        :stacked="true"
        :data="weight_Y"
        :sufix="'milijon ton'"
      ></column-chart>
    </div>
    <div class="chart2">
      <h1>PET NAJBOLJ POGOSTIH POSTOPKOV</h1>
      <column-chart :legend="true" :colors="[chartColor]" :data="process"></column-chart>
    </div>
    <div class="chart3"></div>
    <div class="chart4"></div>
  </div>
</template>

<script>
import http from "../http-common";

export default {
  data: function () {
    return {
      weight_Y: null,
      process: null,
      chartColor: "#3421FF",
      stackedColorsB: true,
      colorsDark: [
        "#89c0b6",
        "#63a6a0",
        "#448c8a",
        "#287274",
        "#0d585f",
      ],
      colorsLight: [
        "#d1afe8",
        "#b998dd",
        "#9f82ce",
        "#826dba",
        "#63589f",
      ],
    };
  },
  methods: {
    getChart1() {
      var months_slo = {
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "Maj",
        6: "Jun",
        7: "Jul",
        8: "Avg",
        9: "Sep",
        10: "Okt",
        11: "Nov",
        12: "Dec",
      };

      var query =
        "SELECT DATE_PART('year', dat_oddaje) as year, DATE_PART('month', dat_oddaje) as month, sum(kol_kg) as weight from evl GROUP BY year, month;";
      console.log(query);
      http
        .get("/trash", { params: { q: query } })
        .then((response) => {
          var helper = {};
          response.data.forEach((e) => {
            helper[e.year] = [];
          });
          response.data.forEach((e) => {
            helper[e.year].push({ month: e.month, weight: e.weight });
          });
          console.log(helper["2017"][0]);
          this.weight_Y = [];
          ["2017", "2018", "2019", "2020", "2021"].forEach((key, index) => {
            console.log(key);
            var builder = {};
            var color_help = '#fff';
            for (let i = 0; i < 12; i++) {
              if (helper[key][i]) {
                builder[months_slo[i + 1]] = helper[key][i].weight / 1000000;
              } else {
                builder[months_slo[i + 1]] = 0;
              }
            }
            color_help = this.colorsDark[index];
            console.log(builder);
            this.weight_Y.push({
              name: key,
              data: builder,
              color: color_help
            });
          });
          console.log(this.weight_Y);
          localStorage.weightForYears = JSON.stringify(this.weight_Y);
        })
        .catch((e) => {
          console.log(e);
          this.loading = false;
        });
    },
    getChart2() {
      var query =
        "SELECT predviden_postopek, sum(kol_kg) AS weight FROM evl GROUP BY predviden_postopek ORDER BY weight DESC LIMIT 5;";
      console.log(query);
      http
        .get("/trash", { params: { q: query } })
        .then((response) => {
          this.process = {};
          response.data.forEach((e) => {
            this.process[e.predviden_postopek.toUpperCase()] =
              e.weight / 1000000;
          });
          console.log(this.process);
          localStorage.top_five_process = JSON.stringify(this.process);
        })
        .catch((e) => {
          console.log(e);
          this.loading = false;
        });
    },
    changeData2() {
      var helper = []
        this.weight_Y.forEach((e, index) => {
            console.log(index)
            console.log(this.stackedColorsB)
            if (this.stackedColorsB == "true") {
                var colorHelper = this.colorsLight[index]
            } else {
                colorHelper = this.colorsDark[index]
            }
            console.log(colorHelper);
            helper.push({
              name: e.name,
              data: e.data,
              color: colorHelper
            });
        });
        this.weight_Y = helper;
        localStorage.weightForYears = JSON.stringify(this.weight_Y);
        console.log(this.weight_Y)
    }
  },
  mounted() {
    this.chartColor = getComputedStyle(
      document.documentElement
    ).getPropertyValue("--accent");
    document
      .getElementById("switch")
      .getElementsByTagName("input")[0]
      .addEventListener("click", () => {
        setTimeout(() => {
          this.chartColor = getComputedStyle(
            document.documentElement
          ).getPropertyValue("--accent");
        }, 100);
      });
      
    if (localStorage.weightForYears) {
      this.weight_Y = JSON.parse(localStorage.weightForYears);
    } else {
      this.getChart1();
    }
    if (localStorage.top_five_process) {
      this.process = JSON.parse(localStorage.top_five_process);
    } else {
      this.getChart2();
    }

    this.stackedColorsB = getComputedStyle(
      document.documentElement
    ).getPropertyValue("--stacked-colors");
    document
      .getElementById("switch")
      .getElementsByTagName("input")[0]
      .addEventListener("click", () => {
        setTimeout(() => {
          this.stackedColorsB = getComputedStyle(
            document.documentElement
          ).getPropertyValue("--stacked-colors");
          console.log(this.stackedColorsB);
          this.changeData2();
        }, 100);
      });
  },
};
</script>

<style lang="sass" scoped>
.four_charts
    min-height: 100%
    display: flex
    flex-wrap: wrap
    flex-direction: row

    & > div
        display: flex
        flex-basis: calc(50% - 40px)
        justify-content: center
        flex-direction: column
</style>