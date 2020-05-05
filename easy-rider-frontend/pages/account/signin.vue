<template>
  <UserLoginPage :error="error" @submit="onSubmit">
    <template v-slot:submit-button-content>
      Sign In
    </template>

    <template v-slot:additional-controls>
      <b-link to="/account/signup" class="mt-2">
        Don't have an account? Sign Up
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
        await this.$store.dispatch('trips/clear')
        await this.$store.dispatch('users/clear')

        await this.$auth.loginWith('local', {
          data: {
            email: user.email,
            password: user.password
          }
        })
      } catch (exception) {
        this.error = exception
      }
    }
  },
  head() {
    return {
      title: 'Easy Rider | Sign In'
    }
  }
}
</script>
