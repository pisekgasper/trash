<template>
  <div class="form" v-if="!loading && !list">
    <span>Pošiljatelj</span>
    <vue3-simple-typeahead
      class="first"
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
    <span>Prejemnik</span>
    <vue3-simple-typeahead
      id="find_receiver"
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
    <div class="selector-container">
      <select name="month" v-model="month">
        <option value="0">Mesec...</option>
        <option value="1">Januar</option>
        <option value="2">Februar</option>
        <option value="3">Marec</option>
        <option value="4">April</option>
        <option value="5">Maj</option>
        <option value="6">Junij</option>
        <option value="7">Julij</option>
        <option value="8">Avgust</option>
        <option value="9">September</option>
        <option value="10">Oktober</option>
        <option value="11">November</option>
        <option value="12">December</option>
      </select>
      <select name="year" v-model="year">
        <option value="2021">2021</option>
        <option value="2020">2020</option>
        <option value="2019">2019</option>
        <option value="2018">2018</option>
        <option value="2017">2017</option>
      </select>
      <select name="danger" v-model="dngr">
        <option value="0">Nevarnost odpadka...</option>
        <option value="true">DA</option>
        <option value="false">NE</option>
      </select>
    </div>
    <div class="button-container">
      <input
        id="FindButton"
        type="button"
        value="POIŠČI"
        @click="getSendersEvl"
        v-if="selected_sender != null"
      />
    </div>
  </div>
  <div class="evl_list" v-if="loading || list">
    <div
      class="close-list"
      v-if="list"
      @click="
        () => {
          list = false;
          loading = false;
          selected_sender = null;
          selected_receiver = null;
        }
      "
    >
      &times;
    </div>
    <p v-if="loading">Loading</p>
    <div class="offset">
      <div class="evls" v-if="list">
        <div
          class="evl_card"
          v-for="p in displayedEvls"
          :key="p.evl_id"
          @click="openModal = p.evl_id"
        >
          <p>MATIČNA ŠTEVILKA EVL: {{ p.evl_id }}</p>
          <p>
            ODDAN:
            {{
              new Date(p.dat_oddaje).toLocaleDateString("sl-SI", {
                day: "numeric",
                month: "long",
                year: "numeric",
              })
            }}
            <span class="ind"
              >SPREJETO:
              <span :style="{ color: p.ind_sprejeto ? 'green' : 'red' }">{{
                p.ind_sprejeto ? "DA" : "NE"
              }}</span></span
            >
          </p>
        </div>
      </div>
      <div
        v-for="p in displayedEvls"
        :key="p.evl_id"
        :class="{ modal: true, hidden: openModal != p.evl_id }"
        id="{{p.evl_id}}"
      >
        <!-- button to close the modal -->
        <button class="close-modal" @click="openModal = 0">&times;</button>
        <h1>EVL matična številka: {{ p.evl_id }}</h1>
        <p>
          <b>POŠILJATELJ:</b> {{ p.sender_id }}
          <span style="float: right"
            ><b>DATUM:</b>
            {{
              new Date(p.dat_oddaje).toLocaleDateString("sl-SI", {
                day: "numeric",
                month: "long",
                year: "numeric",
              })
            }}</span
          >
        </p>
        <p><b>PREJEMNIK:</b> {{ p.receiver_id }}</p>
        <p><b>PREVOZNIK:</b> {{ p.transporter_id }}</p>
        <br /><br />
        <p>
          <b>TIP ODPADKA:</b> {{ p.naziv_odpadka }}
          <span style="float: right"
            ><b>NEVAREN:</b> {{ p.nevaren ? "DA" : "NE" }}</span
          >
        </p>
        <p><b>IZVOR ODPADKA:</b> {{ p.izvor_odpadka.toLowerCase() }}</p>
        <br /><br />
        <p><b>KOLIČINA:</b> {{ p.kol_kg }} kg</p>
        <p><b>POSTOPEK:</b> {{ p.predviden_postopek }}</p>
      </div>

      <nav aria-label="Page navigation example" v-if="list">
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
          <li class="page-item number">
            <button
              type="button"
              class="page-link"
              v-for="pageNumber in pages"
              :key="pageNumber"
              @click="page = pageNumber"
              :class="{ selected: page == pageNumber }"
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
  <div
    v-if="list"
    :class="{ overlay: true, hidden: openModal == 0 }"
    @click="openModal = 0"
  ></div>
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
      month: "0",
      loading: false,
      list: false,
      page: 1,
      perPage: 10,
      pages: [],
      openModal: 0,
      dngr: "0",
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
      var query = `SELECT * FROM evl WHERE sender_id = ${this.selected_sender}`;
      if (this.selected_receiver != null) {
        query = query.concat(`AND receiver_id = ${this.selected_receiver}`);
      }
      if (this.year != null) {
        query = query.concat(
          `AND DATE_PART('year', dat_oddaje) = '${this.year}'`
        );
      }
      if (this.month != "0") {
        query = query.concat(
          `AND DATE_PART('month', dat_oddaje) = '${this.month}'`
        );
      }
      if (this.dngr != "0") {
        //var isTrueSet = (myValue === 'true');
        query = query.concat(`AND nevaren = ${this.dngr}`);
      }

      query = query.concat(` LIMIT 100;`);

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
      this.selected_receiver = null;
    },
    setPages() {
      this.pages = [];
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
    document.getElementsByTagName("html")[0].classList.add("loaded");
    this.borderFill = getComputedStyle(
      document.documentElement
    ).getPropertyValue("--accent");
    console.log(this.borderFill);
    this.getSenders();
    this.getReceivers();
  },
};
</script>

<style lang="scss" scoped>
.button-container {
  display: block;
  width: 100%;
  position: relative;
  margin-top: 3rem;
}
#FindButton {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  width: 50%;
  background-color: var(--accent);
  color: var(--bg-00);
  cursor: pointer;
  margin: auto;
}
#FindButton:hover {
  background-color: var(--bg-02);
  color: var(--content);
  transition: all 0.3s ease-out;
}
.form {
  padding: 4vh 0;
  width: 75%;
  text-align: center;
  margin: auto;
  text-align: left;
}
.form span {
  display: block;
  padding-left: 2rem;
  padding-bottom: 0.4rem;
}
.form span:not(:first-child) {
  margin-top: 3rem;
}
// .form .simple-typeahead:not(.first) {
//   margin-top: 3rem;
// }

.selector-container {
  margin-top: 3rem;
  display: inline-flex;
  width: 100%;
  gap: 2rem;
}
.selector-container select {
  flex: 1;
}

.page-item {
  display: flex;
}
button.page-link {
  display: inline;
}
button.page-link {
  font-size: 20px;
  color: var(--content);
  border-radius: 12px;
  font-weight: 500;
  background-color: var(--bg-02) !important;
  border: 0.15rem solid var(--bg-02);
  padding: 0rem 1rem;
  font-size: 1.3rem;
}

.pagination .number button {
  margin: 0 0.3rem;
}

button.selected {
  color: var(--bg-00) !important;
  background-color: var(--accent) !important;
  border: 0.15rem solid var(--accent);
}

ul.pagination {
  width: 80% !important;
  margin: 0 auto !important;
}

.pagination li {
  display: flex;
}

nav {
  padding-top: 12px;
}

nav ul {
  display: flex;
  justify-content: space-between;
}

button:disabled {
  background-color: var(--font-disabled);
}

.modal {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80%;
  max-width: 500px;
  background-color: var(--bg-00);
  padding: 4rem;
  border-radius: 20px;
  box-shadow: 0 3rem 5rem rgba(0, 0, 0, 0.3);
  z-index: 10;
  //text-align: center;
}

.modal h1 {
  font-size: 1.8rem;
  margin-bottom: 2rem;
  color: var(--content);
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 4vh;
  // background-color: var(--blur-color);
  -webkit-backdrop-filter: blur(55px);
  backdrop-filter: blur(5px);
  z-index: 5;
}

.close-modal {
  position: absolute;
  top: 0.8rem;
  right: 1.3rem;
  font-size: 2.5rem;
  color: var(--accent);
  cursor: pointer;
  border: none;
}

.close-list {
  position: absolute;
  top: 1.8rem;
  right: 4.3rem;
  font-size: 3.5rem;
  color: var(--accent);
  cursor: pointer;
  border: none;
}

button.close-modal {
  background-color: var(--bg-00) !important;
}

/* CLASS TO HIDE MODAL */
.hidden {
  display: none;
}

.evls {
  margin: 0 auto;
  width: 80%;
}

.evl_card {
  padding: 1rem;
  border-color: var(--bg-02);
  border-radius: 20px;
  border-style: solid;
  border-width: 0 1px 1px 1px;
}

.evl_card:hover {
  cursor: pointer;
  background-color: var(--bg-03);
}

.ind {
  float: right;
}
input {
  border-radius: 4vh !important;
}
</style>
