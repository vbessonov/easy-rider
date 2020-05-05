<template>
  <b-container>
    <h3>Create a new user</h3>
    <p>Please specify below all the details of a new user</p>

    <UserEditForm v-model="user" @submit="onSubmit" />
  </b-container>
</template>

<script>
import User from '~/models/User'
import UserEditForm from '~/components/users/UserEditForm'

export default {
  middleware: ['privileged'],
  components: {
    UserEditForm
  },
  data() {
    return {
      user: new User('', '')
    }
  },
  methods: {
    async onSubmit(newUser) {
      const newlyCreatedUser = await this.$store.dispatch(
        'users/create',
        newUser
      )

      this.$router.replace({
        name: 'users',
        params: { newlyCreatedUser }
      })
    }
  },
  head() {
    return {
      title: 'Easy Rider | New User'
    }
  }
}
</script>
