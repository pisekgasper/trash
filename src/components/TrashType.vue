<template>
  <div class="form">
    <select class="waste_type" name="type" v-model="type">
      <option v-for="t in all_types" :value="t" :key="t">{{ t }}</option>
    </select>
    <select class="year" name="year" v-model="year">
      <option value="2021">2021</option>
      <option value="2020">2020</option>
      <option value="2019">2019</option>
      <option value="2018">2018</option>
      <option value="2017">2017</option>
    </select>
  </div>
  <div class="graphs">
    <column-chart :colors="[chartColor]" :data="monthly_data"></column-chart>
  </div>
</template>

<script>
import http from "../http-common";

export default {
  data: function () {
    return {
      type: "",
      year: "2021",
      all_types: null,
      loading: true,
      monthly_data: null,
      chartColor: "#3421FF",
    };
  },
  methods: {
    getTypes() {
      var query = "SELECT DISTINCT naziv_odpadka AS type FROM evl;";
      console.log(query);
      http
        .get("/trash", { params: { q: query } })
        .then((response) => {
          this.all_types = [];
          response.data.forEach((e) => {
            this.all_types.push(e.type);
          });
          console.log(this.all_types);
          localStorage.wasteTypes = JSON.stringify(this.all_types);
        })
        .catch((e) => {
          console.log(e);
          this.loading = false;
        });
    },
    getYearlyProduce() {
      var query = `SELECT DATE_PART('month',dat_oddaje) AS month, sum(kol_kg) AS weight FROM evl WHERE DATE_PART('year',dat_oddaje) = '${this.year}' AND naziv_odpadka LIKE '${this.type}' GROUP BY month;`;

      http
        .get("/trash", { params: { q: query } })
        .then((response) => {
          console.log(response);
          this.monthly_data = {};
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
          response.data.forEach((e) => {
            this.monthly_data[months_slo[e.month]] = e.weight;
          });
          for (const [_, value] of Object.entries(months_slo)) {
            if (this.monthly_data[value] == null) {
              this.monthly_data[value] = 0;
              console.log(_)
            }
          }
          console.log(this.monthly_data);
        })
        .catch((e) => {
          console.log(e);
          this.loading = false;
        });
    },
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
    if (localStorage.wasteTypes) {
      this.all_types = JSON.parse(localStorage.wasteTypes);
    } else {
      this.getTypes();
    }
  },
  watch: {
    type: function () {
      this.getYearlyProduce();
    },
    year: function () {
      this.getYearlyProduce();
    },
  },
};
</script>

<style lang="scss" scoped>
.graphs {
  margin-top: 3vh;
}
.form {
  display: inline-flex;
  width: 100%;
}
select.waste_type {
  width: 100%;
  max-width: 100%;
  flex: 1;
  margin-right: 3vh;
}
</style>
