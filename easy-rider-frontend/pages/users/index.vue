<template>
  <b-container>
    <b-alert
      v-if="newlyCreatedUser !== null"
      :show="newlyCreatedUser !== null"
      variant="success"
      dismissible
    >
      User
      <b-link :to="`/users/${newlyCreatedUser.id}`">
        {{ newlyCreatedUser.email }}
      </b-link>
      has been successfully created
    </b-alert>

    <Alert :error="error" />

    <h3>List of users</h3>

    <p>
      You can filter users using the controls below
    </p>

    <UserTable
      :users="userList"
      @add="onAdd"
      @edit="onEdit"
      @delete="onDelete"
    />
  </b-container>
</template>

<script>
import { mapGetters } from 'vuex'
import Alert from '~/components/Alert'
import UserTable from '~/components/users/UserTable'

export default {
  middleware: ['privileged'],
  components: {
    Alert,
    UserTable
  },
  async asyncData({ store, error }) {
    try {
      const users = await store.dispatch('users/list')
      return { users }
    } catch (exception) {
      error({ statusCode: 404, message: 'Users were not found' })
    }
  },
  data() {
    return {
      newlyCreatedUser: this.$route.params.newlyCreatedUser || null,
      users: [],
      error: null
    }
  },
  computed: {
    ...mapGetters('users', ['userList'])
  },
  methods: {
    onAdd() {
      this.$router.push('/users/add')
    },
    onEdit(user) {
      this.$router.push(`/users/${user.id}`)
    },
    async onDelete(user) {
      const result = await this.$bvModal.msgBoxConfirm(
        `Are you sure you want to delete user ${user.email}?`,
        {
          title: 'Confirmation'
        }
      )

      if (result) {
        this.error = null

        try {
          await this.$store.dispatch('users/destroy', user)
        } catch (exception) {
          this.error = exception
        }
      }
    }
  },
  head() {
    return {
      title: 'Easy Rider | Users'
    }
  }
}
</script>
