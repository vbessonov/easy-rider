<template>
  <b-container>
    <h3>User details</h3>

    <p>
      Please update the user details provided below or update
      <b-link :to="`/users/${user.id}/trips`">user trips</b-link>
    </p>

    <Alert :error="error" />

    <UserEditForm v-model="user" @submit="onSubmit" @cancel="onCancel">
      <template v-slot:submit-button-content>
        Save
      </template>
    </UserEditForm>
  </b-container>
</template>

<script>
import User from '~/models/User'
import Alert from '~/components/Alert'
import UserEditForm from '~/components/users/UserEditForm'

export default {
  middleware: ['privileged'],
  components: {
    Alert,
    UserEditForm
  },
  async asyncData({ store, route, error }) {
    try {
      const userId = route.params.userId
      const retrievedUser = await store.dispatch('users/retrieve', userId)
      const user = new User(
        retrievedUser.id,
        retrievedUser.email,
        retrievedUser.password,
        retrievedUser.role
      )

      return { user }
    } catch (exception) {
      error({ statusCode: 404, message: 'User was not found' })
    }
  },
  data() {
    return {
      user: new User(),
      error: null
    }
  },
  methods: {
    async onSubmit() {
      this.error = null

      try {
        await this.$store.dispatch('users/update', this.user)

        this.$router.replace('/users')
      } catch (exception) {
        this.error = exception
      }
    },
    onCancel() {
      this.$router.replace('/users')
    }
  },
  head() {
    return {
      title: 'Easy Rider | Edit User'
    }
  }
}
</script>
