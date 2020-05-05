<template>
  <b-container>
    <h3>Trip details</h3>

    <p>
      Please update the trip details provided below
    </p>

    <Alert :error="error" />

    <TripEditForm
      v-model="trip"
      :readonly="readonly"
      @submit="onSubmit"
      @cancel="onCancel"
    >
      <template v-slot:submit-button-content>
        Save
      </template>
    </TripEditForm>
  </b-container>
</template>

<script>
import { mapState, mapGetters } from 'vuex'
import Trip from '~/models/Trip'
import Alert from '~/components/Alert'
import TripEditForm from '~/components/trips/TripEditForm'

export default {
  components: {
    Alert,
    TripEditForm
  },
  async asyncData({ store, route, error }) {
    try {
      const userId = route.params.userId
      const tripId = route.params.tripId
      const trip = await store.dispatch('trips/retrieve', { userId, tripId })
      const tripCopy = Object.assign({}, trip)

      return { trip: tripCopy }
    } catch (exception) {
      error({ statusCode: 404, message: 'User was not found' })
    }
  },
  data() {
    return {
      trip: new Trip(),
      userId: parseInt(this.$route.params.userId),
      error: null
    }
  },
  computed: {
    ...mapState('auth', ['user']),
    ...mapGetters('account', ['isAdmin']),
    isAuthor() {
      return this.user.id === this.userId
    },
    readonly() {
      return !this.isAuthor && !this.isAdmin
    }
  },
  methods: {
    async onSubmit() {
      this.error = null

      try {
        await this.$store.dispatch('trips/update', {
          userId: this.userId,
          trip: this.trip
        })

        this.$router.replace(`/users/${this.userId}/trips`)
      } catch (exception) {
        this.error = exception
      }
    },
    onCancel() {
      this.$router.replace(`/users/${this.userId}/trips`)
    }
  },
  head() {
    return {
      title: 'Easy Rider | Edit Trip'
    }
  }
}
</script>
