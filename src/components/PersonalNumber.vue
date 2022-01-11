<template>
  <div class="form">
    <vue3-simple-typeahead
      id="find_sender"
      placeholder="Išči pošiljatelja ali prejemnika..."
      :items="senders"
    >
    </vue3-simple-typeahead>
  </div>
</template>

<script>
export default {
  data: function () {
    return {
      senders: null,
      receivers: null,
    };
  },
  methods: {
    getSenders() {
      if (this.senders != null) {
        return;
      }
      var query = "SELECT id, name FROM senders;";
      console.log(query);
      http
        .get("/trash", { params: { q: query } })
        .then((response) => {
          this.senders = [];
          response.data.forEach((e) => {
            this.senders.push(e.name);
          });
          console.log(this.senders);
        })
        .catch((e) => {
          console.log(e);
          this.loading = false;
        });
    },
  },
  mounted() {
      this.getSenders();
  }
};
</script>

<style>
</style>