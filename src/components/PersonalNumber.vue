<template>
  <div class="form" v-if="!loading && !list">
    <vue3-simple-typeahead
      id="find_sender"
      placeholder="Išči pošiljatelja..."
      :items="senders"
      :itemProjection="
        (item) => {
          return item.name;
        }
      "
      @selectItem="
        (item) => {
          selected_sender = item.id;
          sender_name = item.name;
        }
      "
    >
    </vue3-simple-typeahead>
    <vue3-simple-typeahead
      id="find_sender"
      placeholder="Išči prejemnika..."
      :items="receivers"
      :itemProjection="
        (item) => {
          return item.name;
        }
      "
      @selectItem="
        (item) => {
          selected_receiver = item.id;
          receiver_name = item.name;
        }
      "
    >
    </vue3-simple-typeahead>
    <select name="year" v-model="year">
      <option value="2021">2021</option>
      <option value="2020">2020</option>
      <option value="2019">2019</option>
      <option value="2018">2018</option>
      <option value="2017">2017</option>
    </select>
    <input
      type="button"
      value="POIŠČI"
      @click="getSendersEvl"
      v-if="selected_sender != null"
    />
  </div>
  <div class="evl_list" v-if="loading || list">
    <p v-if="loading">Loading</p>
    <div class="offset">
      <table class="table table-bordered" v-if="list">
        <thead>
          <tr>
            <th>ID evl</th>
            <th>ID pošiljatelja</th>
            <th>Datum oddaje</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in displayedEvls" :key="p.evl_id">
            <td>{{ p.evl_id }}</td>
            <td>{{ p.sender_id }}</td>
            <td>{{ p.dat_oddaje }}</td>
          </tr>
        </tbody>
      </table>
      <nav aria-label="Page navigation example">
        <ul class="pagination">
          <li class="page-item">
            <button
              type="button"
              class="page-link"
              :disabled="page == 1"
              @click="page--"
            >
              Previous
            </button>
          </li>
          <li class="page-item">
            <button
              type="button"
              class="page-link"
              v-for="pageNumber in pages.slice(page - 1, page + 4)"
              :key="pageNumber"
              @click="page = pageNumber"
              :style="{ color: page == pageNumber ? 'red' : 'green' }"
            >
              {{ pageNumber }}
            </button>
          </li>
          <li class="page-item">
            <button
              type="button"
              @click="page++"
              :disabled="page == pages.length"
              class="page-link"
            >
              Next
            </button>
          </li>
        </ul>
      </nav>
    </div>
  </div>
</template>

<script>
import http from "../http-common";

export default {
  data: function () {
    return {
      senders: null,
      receivers: null,
      selected_sender: null,
      sender_name: null,
      selected_receiver: null,
      receiver_name: null,
      evls: null,
      year: "2021",
      loading: false,
      list: false,
      page: 1,
      perPage: 9,
      pages: [],
    };
  },
  methods: {
    getSenders() {
      if (this.senders != null) {
        return;
      }
      var query = "SELECT id, name FROM sender;";
      console.log(query);
      http
        .get("/trash", { params: { q: query } })
        .then((response) => {
          this.senders = [];
          response.data.forEach((e) => {
            this.senders.push({ name: e.name, id: e.id });
          });
          console.log(this.senders);
        })
        .catch((e) => {
          console.log(e);
          this.loading = false;
        });
    },
    getReceivers() {
      if (this.receivers != null) {
        return;
      }
      var query = "SELECT id, name FROM receiver;";
      console.log(query);
      http
        .get("/trash", { params: { q: query } })
        .then((response) => {
          this.receivers = [];
          response.data.forEach((e) => {
            this.receivers.push({ name: e.name, id: e.id });
          });
          console.log(this.receivers);
        })
        .catch((e) => {
          console.log(e);
          this.loading = false;
        });
    },
    getSendersEvl() {
      if (this.selected_receiver != null) {
        var query = `SELECT * FROM evl WHERE sender_id = ${this.selected_sender} AND receiver_id = ${this.selected_receiver} AND DATE_PART('year',dat_oddaje) = '${this.year}';`;
      } else {
        query = `SELECT * FROM evl WHERE sender_id = ${this.selected_sender} AND DATE_PART('year',dat_oddaje) = '${this.year}';`;
      }
      this.loading = !this.loading;
      console.log(query);
      http
        .get("/trash", { params: { q: query } })
        .then((response) => {
          this.evls = [];
          response.data.forEach((e) => {
            this.evls.push(e);
          });
          if (this.evls.length != 0) {
            this.list = true;
            this.setPages();
          }
          this.loading = !this.loading;

          console.log(this.evls);
        })
        .catch((e) => {
          console.log(e);
          this.loading = false;
        });
    },
    setPages() {
      let numberOfPages = Math.ceil(this.evls.length / this.perPage);
      for (let index = 1; index <= numberOfPages; index++) {
        this.pages.push(index);
      }
    },
    paginate(evls) {
      let page = this.page;
      let perPage = this.perPage;
      let from = page * perPage - perPage;
      let to = page * perPage;
      return evls.slice(from + 1, to);
    },
  },
  computed: {
    displayedEvls() {
      return this.paginate(this.evls);
    },
  },
  mounted() {
    this.getSenders();
    this.getReceivers();
  },
};
</script>

<style lang="scss" scoped>
button.page-link {
	display: inline-block;
}
button.page-link {
    font-size: 20px;
    color: #29b3ed;
    font-weight: 500;
}
</style>
