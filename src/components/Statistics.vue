<template>
  <div class="four_charts">
    <div class="chart1">
      <column-chart ytitle="Teža v Mt" :stacked="true" :data="weight_Y"></column-chart>
    </div>
    <div class="chart2"></div>
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
    };
  },
  methods: {
    getChart1() {
        var months_slo = {
            1: "Januar",
            2: "Februar",
            3: "Marec",
            4: "April",
            5: "Maj",
            6: "Junij",
            7: "Julij",
            8: "Avgust",
            9: "September",
            10: "Oktober",
            11: "November",
            12: "December",
          };

      var query = "SELECT DATE_PART('year', dat_oddaje) as year, DATE_PART('month', dat_oddaje) as month, sum(kol_kg) as weight from evl GROUP BY year, month;";
      console.log(query);
      http
        .get("/trash", { params: { q: query } })
        .then((response) => {
          var helper = {};
          response.data.forEach((e) => {
            helper[e.year] = [];
          });
          response.data.forEach((e) => {
            helper[e.year].push({month: e.month, weight: e.weight});
          });
          console.log(helper['2017'][0]);
          this.weight_Y = [];
          ["2017", "2018", "2019", "2020", "2021"].forEach(key => {
              console.log(key);
              var builder = {}
              for (let i = 0; i < 12; i++) {
                  if (helper[key][i]) {
                    builder[months_slo[i+1]] = helper[key][i].weight / 1000000;
                  } else {
                      builder[months_slo[i+1]] = 0;
                  }
                  
                  
              }
              console.log(builder)
              this.weight_Y.push({
                  name: key, 
                  data: builder,
              })
          });
          console.log(this.weight_Y);
          localStorage.weightForYears = JSON.stringify(this.weight_Y);
        })
        .catch((e) => {
          console.log(e);
          this.loading = false;
        });
    },
  },
  mounted() {
      if (localStorage.weightForYears) {
          this.weight_Y = JSON.parse(localStorage.weightForYears);
      } else {
          this.getChart1();
      }
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