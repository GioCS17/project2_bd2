<template>
  <div>
    <b-container>
        <h1>Tweets</h1>
        <b-button variant="primary" v-b-modal.modal-index>Load Files to create Inverted Index</b-button>

        <b-modal id="modal-index" size="lg" ok-only>
          <LoadFiles />
        </b-modal>
        <hr>
        <b-form-input v-model="text" placeholder="Enter your query"></b-form-input>
        <br>
        <b-button v-if="spinner" @click="search(text)" variant="primary">Search</b-button>
        <b-button v-else variant="primary" disabled>
          <b-spinner small type="grow"></b-spinner>
          Searching...
        </b-button>
        <div class="mt-2">Value: {{ text }}</div>
        <b-card v-for="(m, idx) in msg" :key="idx" :img-src="m.profile_image_url" img-left>
            <b-button href="#" variant="success">
                {{ m.name }}
            </b-button>
            <b-card-text>
                {{ m.text }}
            </b-card-text>
        </b-card>
    </b-container>
  </div>
</template>

<script>
import axios from 'axios';
import LoadFiles from '@/components/LoadFiles.vue'

export default {
  name: 'Tweets',
  components: {
    LoadFiles
  },
  data() {
    return {
      msg: [],
      text: '',
      spinner : true
    };
  },
  methods: {
    async search(to_search) {
      this.spinner = false
      const path = 'http://localhost:5000/tweets/' + to_search;
      await axios.get(path)
        .then((res) => {
          this.msg = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
      this.spinner = true
    }
  }
};
</script>