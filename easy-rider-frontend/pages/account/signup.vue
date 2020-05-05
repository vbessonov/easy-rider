<template>
  <UserLoginPage :error="error" @submit="onSubmit">
    <template v-slot:submit-button-content>
      Sign Up
    </template>

    <template v-slot:additional-controls>
      <b-link to="/account/signin" class="mt-2">
        Already an Easy Rider user? Sign In
      </b-link>
    </template>
  </UserLoginPage>
</template>

<script>
import UserLoginPage from '~/components/users/UserLoginPage'

export default {
  auth: 'guest',
  layout: 'simple',
  components: {
    UserLoginPage
  },
  data() {
    return {
      error: null
    }
  },
  methods: {
    async onSubmit(user) {
      this.error = null

      try {
        this.$store.dispatch('trips/clear')
        this.$store.dispatch('users/clear')

        await this.$axios.$post('/users/', user)

        await this.$auth.loginWith('local', {
          data: user
        })

        this.$router.push('/')
      } catch (exception) {
        this.error = exception
      }
    }
  },
  head() {
    return {
      title: 'Easy Rider | Sign Up'
    }
  }
}
</script>
