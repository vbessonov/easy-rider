<template>
  <b-container>
    <b-alert
      v-if="newlyCreatedTrip !== null"
      :show="newlyCreatedTrip !== null"
      variant="success"
      dismissible
    >
      Trip
      <b-link :to="`/users/${userId}/trips/${newlyCreatedTrip.id}`">
        {{ newlyCreatedTrip.destination }}
      </b-link>
      has been successfully created
    </b-alert>

    <h3>List of trips</h3>

    <p>
      You can filter trips using the controls below and
      <b-link @click="onPrint">print your itinerary</b-link> after
    </p>

    <TripTable
      :readonly="readonly"
      :user-id="userId"
      :trips="tripList(userId)"
      :destination-filter.sync="filters.destinationFilter"
      :start-date-start-filter.sync="filters.startDateStartFilter"
      :start-date-end-filter.sync="filters.startDateEndFilter"
      :end-date-start-filter.sync="filters.endDateStartFilter"
      :end-date-end-filter.sync="filters.endDateEndFilter"
      @add="onAdd"
      @edit="onEdit"
      @delete="onDelete"
    />
  </b-container>
</template>

<script>
import { mapState, mapGetters } from 'vuex'
import TripTable from '~/components/trips/TripTable.vue'
import { dateToString } from '~/utils/date'

export default {
  components: {
    TripTable
  },
  async asyncData({ store, route, error }) {
    try {
      const trips = await store.dispatch('trips/list', route.params.userId)

      return { trips }
    } catch (exception) {
      error({ statusCode: 404, message: 'Trips were not found' })
    }
  },
  data() {
    return {
      newlyCreatedTrip: this.$route.params.newlyCreatedTrip || null,
      userId: parseInt(this.$route.params.userId),
      trips: [],
      filters: {
        destinationFilter: '',
        startDateStartFilter: null,
        startDateEndFilter: null,
        endDateStartFilter: null,
        endDateEndFilter: null
      }
    }
  },
  computed: {
    ...mapState('auth', ['user']),
    ...mapGetters('account', ['isAdmin']),
    ...mapGetters('trips', ['tripList']),
    isAuthor() {
      return this.user.id === this.userId
    },
    readonly() {
      return !this.isAuthor && !this.isAdmin
    }
  },
  methods: {
    onAdd() {
      this.$router.push(`/users/${this.userId}/trips/add`)
    },
    onEdit(trip) {
      this.$router.push(`/users/${this.userId}/trips/${trip.id}`)
    },
    async onDelete(trip) {
      const result = await this.$bvModal.msgBoxConfirm(
        `Are you sure you want to delete trip to ${trip.destination}?`,
        {
          title: 'Confirmation'
        }
      )

      if (result) {
        this.$store.dispatch('trips/destroy', {
          userId: this.userId,
          tripId: trip.id
        })
      }
    },
    onPrint() {
      const route = this.$router.resolve({
        name: 'users-userId-trips-itinerary',
        params: this.$route.params,
        query: {
          destinationFilter: this.filters.destinationFilter,
          startDateStartFilter: dateToString(this.filters.startDateStartFilter),
          startDateEndFilter: dateToString(this.filters.startDateEndFilter),
          endDateStartFilter: dateToString(this.filters.endDateStartFilter),
          endDateEndFilter: dateToString(this.filters.endDateEndFilter)
        }
      })

      window.open(route.href, '_blank')
    }
  },
  head() {
    return {
      title: 'Easy Rider | Trips'
    }
  }
}
</script>
