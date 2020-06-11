<template>
  <div class="home">
    <Tweets />
  </div>
</template>

<script>
// @ is an alias to /src
import Tweets from '@/components/Tweets.vue'

export default {
  name: 'Home',
  components: {
    Tweets
  }
}
</script>
