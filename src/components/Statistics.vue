<template>
  <div class="four_charts">
    <div class="chart1">
      <line-chart :data="weight_Y"></line-chart>
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
      var query = "SELECT DATE_PART('year', dat_oddaje) as year, DATE_PART('month', dat_oddaje) as month, sum(kol_kg) as weight from evl GROUP BY year, month;";
      console.log(query);
      http
        .get("/trash", { params: { q: query } })
        .then((response) => {
          this.weight_Y = {};
          response.data.forEach((e) => {
            this.weight_Y[e.year] = [];
          });
          response.data.forEach((e) => {
            this.weight_Y[e.year].push({month: e.month, weight: e.weight});
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