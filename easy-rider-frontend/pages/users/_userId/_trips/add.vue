<template>
  <b-container>
    <h3>Create a new trip</h3>
    <p>Please specify below all the details of a new trip</p>

    <TripEditForm v-model="trip" @submit="onSubmit" @cancel="onCancel" />
  </b-container>
</template>

<script>
import Trip from '~/models/Trip'
import TripEditForm from '~/components/trips/TripEditForm'

export default {
  components: {
    TripEditForm
  },
  data() {
    return {
      trip: new Trip('', null, null, ''),
      userId: parseInt(this.$route.params.userId)
    }
  },
  methods: {
    async onSubmit(trip) {
      const newlyCreatedTrip = await this.$store.dispatch('trips/create', {
        userId: this.userId,
        trip
      })

      this.$router.replace({
        name: 'users-userId-trips',
        params: { newlyCreatedTrip }
      })
    },
    onCancel() {
      this.$router.replace(`/users/${this.userId}/trips`)
    }
  },
  head() {
    return {
      title: 'Easy Rider | New trip'
    }
  }
}
</script>
