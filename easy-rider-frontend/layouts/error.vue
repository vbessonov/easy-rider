<template>
  <div
    id="container"
    class="d-flex flex-column justify-content-center align-items-center text-center"
  >
    <div v-if="error.statusCode === 404">
      <h1>
        OOPS! PAGE NOT FOUND
      </h1>
      <p>
        The page you are looking for might have been removed had its name
        changed or is temporarily unavailable.
      </p>
    </div>
    <div v-else>
      <h1>
        OOPS! THERE WAS AN ERROR
      </h1>
      <p>
        An unexpected error occurred. We are working on it. Stay with us!
      </p>
    </div>
    <b-button to="/" variant="light">
      GO TO HOME PAGE
    </b-button>
  </div>
</template>

<script>
export default {
  layout: 'simple',
  props: {
    error: {
      type: Object,
      required: true
    }
  },
  head() {
    return {
      title: 'Easy Rider | Error'
    }
  }
}
</script>

<style scoped>
#container {
  background-image: url('/images/error.jpg');
  background-position: center;
  background-size: cover;
  position: relative;
}

#container h1,
p {
  color: whitesmoke;
}

/* #container p {
  color: whitesmoke;
} */
</style>
