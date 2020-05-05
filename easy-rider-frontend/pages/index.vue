<template>
  <div
    id="container"
    class="d-flex flex-column justify-content-center align-items-center text-center"
  >
    <b-jumbotron class="main">
      <template v-slot:header>
        <span>
          Plan your next trip now
        </span>
      </template>
      <template v-slot:lead>
        <span>
          It's easy!
        </span>
      </template>
      <b-button v-if="!loggedIn" to="/account/signup" variant="primary">
        Sign Up-It's Free!
      </b-button>
      <b-button v-else :to="`/users/${user.id}/trips`" variant="primary">
        Start now
      </b-button>
    </b-jumbotron>
  </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex'

export default {
  auth: false,
  computed: {
    ...mapState('auth', ['loggedIn', 'user']),
    ...mapGetters('account', ['isPrivileged'])
  },
  head() {
    return {
      title: 'Easy Rider | Home'
    }
  }
}
</script>

<style scoped>
.jumbotron {
  background-color: transparent !important;
  background-image: linear-gradient(
    to bottom,
    rgba(255, 255, 0, 0.1) 0%,
    rgba(255, 255, 255, 0.6) 100%
  );
}

#container {
  background-image: url('/images/background-2.jpg');
  background-position: center;
  background-size: cover;
  position: relative;
}
</style>
