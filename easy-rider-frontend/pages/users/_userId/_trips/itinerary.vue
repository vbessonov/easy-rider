<template>
  <b-container>
    <h3>Your itinerary</h3>

    <p class="non-printable">You can <b-link v-print>print it</b-link></p>

    <div v-if="loading" class="text-center">
      <b-spinner label="Loading..." />
    </div>

    <TripTable
      v-show="!loading"
      :user-id="userId"
      :trips="trips"
      :filterable="false"
      :readonly="true"
      :pagination="false"
      :destination-filter.sync="filters.destinationFilter"
      :start-date-start-filter.sync="filters.startDateStartFilter"
      :start-date-end-filter.sync="filters.startDateEndFilter"
      :end-date-start-filter.sync="filters.endDateStartFilter"
      :end-date-end-filter.sync="filters.endDateEndFilter"
      @filtered="onFiltered"
    />
  </b-container>
</template>

<script>
import TripTable from '~/components/trips/TripTable'

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
      userId: parseInt(this.$route.params.userId),
      trips: [],
      loading: true,
      filters: {
        destinationFilter: this.$route.query.destinationFilter || '',
        startDateStartFilter: this.getDateFilter(
          this.$route.query.startDateStartFilter
        ),
        startDateEndFilter: this.getDateFilter(
          this.$route.query.startDateEndFilter
        ),
        endDateStartFilter: this.getDateFilter(
          this.$route.query.endDateStartFilter
        ),
        endDateEndFilter: this.getDateFilter(this.$route.query.endDateEndFilter)
      }
    }
  },
  mounted() {
    if (
      this.filters.destinationFilter === '' &&
      this.filters.startDateStartFilter === null &&
      this.filters.startDateEndFilter === null &&
      this.filters.endDateStartFilter === null &&
      this.filters.endDateEndFilter === null
    ) {
      this.loading = false
      this.print()
    }
  },
  methods: {
    getDateFilter(filterValue) {
      if (!filterValue) {
        return null
      }

      return new Date(filterValue)
    },
    print() {
      this.$nextTick(() => {
        window.print()
      })
    },
    onFiltered() {
      this.loading = false
      this.print()
    }
  },
  head() {
    return {
      title: 'Easy Rider | Print Itinerary'
    }
  }
}
</script>

<style scoped>
@media print {
  p {
    display: none;
  }
}
</style>
