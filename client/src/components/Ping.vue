<template>
  <div>
    <LoadFiles />
  </div>
</template>

<script>
import axios from 'axios';
import LoadFiles from '@/components/LoadFiles.vue'

export default {
  name: 'Ping',
  components: {
    LoadFiles
  },
  data() {
    return {
      msg: '',
    };
  },
  methods: {
    getMessage() {
      const path = 'http://localhost:5000/ping';
      axios.get(path)
        .then((res) => {
          this.msg = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getMessage();
  },
};
</script>