<template>
  <Table
    :fields="fields"
    :items="trips"
    :filterable="filterable"
    :readonly="readonly"
    :pagination="pagination"
    :busy="busy"
    :filter-function="filter"
    :filter="filterValue"
    @filtered="onFiltered"
    v-on="$listeners"
  >
    <template v-slot:filter>
      <TripFilterForm
        ref="tripFilterForm"
        :destination-filter.sync="currentDestinationFilter"
        :start-date-start-filter.sync="currentStartDateStartFilter"
        :start-date-end-filter.sync="currentStartDateEndFilter"
        :end-date-start-filter.sync="currentEndDateStartFilter"
        :end-date-end-filter.sync="currentEndDateEndFilter"
        :filter-value.sync="filterValue"
        class="mb-1"
      />
    </template>

    <template v-slot:cell(destination)="row">
      <b-link :to="`/users/${userId}/trips/${row.item.id}`">
        {{ row.item.destination }}
      </b-link>
    </template>
  </Table>
</template>

<script>
import { mapState } from 'vuex'
import Table from '~/components/Table'
import TripFilterForm, {
  filter as tripFilterFormFilter
} from '~/components/trips/TripFilterForm'

export default {
  components: {
    Table,
    TripFilterForm
  },
  props: {
    userId: {
      type: Number,
      required: true
    },
    trips: {
      type: Array,
      required: true
    },
    filterable: {
      type: Boolean,
      default: true
    },
    readonly: {
      type: Boolean,
      default: false
    },
    pagination: {
      type: Boolean,
      default: true
    },
    destinationFilter: {
      type: String,
      required: false,
      default: ''
    },
    startDateStartFilter: {
      validator: (prop) => prop instanceof Date || prop === null,
      required: false,
      default: null
    },
    startDateEndFilter: {
      validator: (prop) => prop instanceof Date || prop === null,
      required: false,
      default: null
    },
    endDateStartFilter: {
      validator: (prop) => prop instanceof Date || prop === null,
      required: false,
      default: null
    },
    endDateEndFilter: {
      validator: (prop) => prop instanceof Date || prop === null,
      required: false,
      default: null
    }
  },
  data() {
    return {
      fields: [
        { key: 'destination', label: 'Destination', sortable: true },
        {
          key: 'startDate',
          label: 'Start Date',
          formatter: (value, key, item) => {
            if (item) {
              return item.startDate.toLocaleDateString(this.locale)
            } else {
              return ''
            }
          },
          sortable: true,
          sortByFormatted: false
        },
        {
          key: 'endDate',
          label: 'End Date',
          formatter: (value, key, item) => {
            if (item) {
              return item.endDate.toLocaleDateString(this.locale)
            } else {
              return ''
            }
          },
          sortable: true
        },
        {
          key: 'daysToStart',
          label: 'Days to start',
          formatter: (value, key, item) => {
            if (item) {
              return this.calculateDaysToStart(item)
            } else {
              return 0
            }
          },
          sortable: true,
          sortByFormatted: true,
          filterByFormatted: true
        },
        { key: 'comment', label: 'Comment', sortable: false }
      ],
      filterValue: null,
      busy: false
    }
  },
  computed: {
    ...mapState('account', ['locale']),
    currentDestinationFilter: {
      get() {
        return this.destinationFilter
      },
      set(value) {
        this.$emit('update:destinationFilter', value)
      }
    },
    currentStartDateStartFilter: {
      get() {
        return this.startDateStartFilter
      },
      set(value) {
        this.$emit('update:startDateStartFilter', value)
      }
    },
    currentStartDateEndFilter: {
      get() {
        return this.startDateEndFilter
      },
      set(value) {
        this.$emit('update:startDateEndFilter', value)
      }
    },
    currentEndDateStartFilter: {
      get() {
        return this.endDateStartFilter
      },
      set(value) {
        this.$emit('update:endDateStartFilter', value)
      }
    },
    currentEndDateEndFilter: {
      get() {
        return this.endDateEndFilter
      },
      set(value) {
        this.$emit('update:endDateEndFilter', value)
      }
    }
  },
  methods: {
    calculateDaysToStart(trip) {
      const startDate = new Date(trip.startDate)
      const now = new Date()

      if (startDate <= now) {
        return 0
      }

      const timeDiff = Math.abs(now.getTime() - startDate.getTime())
      const daysDiff = Math.ceil(timeDiff / (1000 * 3600 * 24))

      return daysDiff
    },
    filter(item, filterValue) {
      // if (!this.busy) {
      //   this.busy = true
      // }

      return tripFilterFormFilter(
        this.currentDestinationFilter,
        this.currentStartDateStartFilter,
        this.currentStartDateEndFilter,
        this.currentEndDateStartFilter,
        this.currentEndDateEndFilter,
        item,
        filterValue
      )
    },
    onFiltered() {
      // this.$nextTick(() => {
      //   if (this.busy) {
      //     this.busy = false
      //   }
      // })

      this.$emit('filtered')
    }
  }
}
</script>
