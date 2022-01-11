<template>
  <div class="form">
    <select name="type" v-model="type">
      <option v-for="t in all_types" :value="t" :key="t">{{ t }}</option>
    </select>
    <select name="year" v-model="year">
      <option value="2021">2021</option>
      <option value="2020">2020</option>
      <option value="2019">2019</option>
      <option value="2018">2018</option>
      <option value="2017">2017</option>
    </select>
  </div>
  <div class="graphs">
    <line-chart :data="monthly_data"></line-chart>
  </div>
</template>

<script>
import http from "http";

export default {
  data: function () {
    return {
      type: "",
      year: "2021",
      all_types: null,
      loading: true,
      monthly_data: null,
    };
  },
  methods: {
    getTypes() {
      var query = "SELECT DISTINCT naziv_odpadka AS type FROM evl;";
      console.log(query);
      http
        .get("http://91.236.1.204:8080/api/trash", { params: { q: query } })
        .then((response) => {
          this.all_types = [];
          response.data.forEach((e) => {
            this.all_types.push(e.type);
          });
          console.log(this.all_types);
        })
        .catch((e) => {
          console.log(e);
          this.loading = false;
        });
    },
    getYearlyProduce() {
      var query =
        "SELECT DATE_PART('month',dat_oddaje) AS month, sum(kol_kg) AS weight \
         FROM evl \
         WHERE DATE_PART('year',dat_oddaje) = '" +
        this.year.toString +
        "' AND naziv_odpadka LIKE " +
        this.type +
        " \
         GROUP BY mesec;";

      http
        .get("/trash", { params: { q: query } })
        .then((response) => {
          this.monthly_data = {};
          response.data.forEach((e) => {
            this.monthly_data[e.month] = e.weight;
          });
          console.log(this.monthly_data);
        })
        .catch((e) => {
          console.log(e);
          this.loading = false;
        });
    },
  },
  mounted() {
    this.getTypes();
  },
};
</script>

<style lang="scss" scoped></style>
