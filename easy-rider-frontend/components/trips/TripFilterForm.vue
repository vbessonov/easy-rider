<template>
  <div>
    <b-row>
      <b-col cols="12">
        <TripDestinationInput
          v-model="currentDestinationFilter"
          placeholder="Start typing to filter trips by a destination"
          label="Destination:"
        />
      </b-col>
    </b-row>

    <b-row>
      <b-col cols="6">
        <TripDateInput
          id="start-date-start-input"
          v-model="currentStartDateStartFilter"
          label="Start date (from):"
          placeholder="Select the earliest start date"
        />
      </b-col>
      <b-col cols="6">
        <TripDateInput
          id="start-date-end-input"
          v-model="currentStartDateEndFilter"
          label="Start date (to):"
          placeholder="Select the latest start date"
        />
      </b-col>
    </b-row>

    <b-row>
      <b-col cols="6">
        <TripDateInput
          id="end-date-start-input"
          v-model="currentEndDateStartFilter"
          label="End date (from):"
          placeholder="Select the earliest end date"
        />
      </b-col>
      <b-col cols="6">
        <TripDateInput
          id="end-date-end-input"
          v-model="currentEndDateEndFilter"
          label="End date (to):"
          placeholder="Select the earliest end date"
        />
      </b-col>
    </b-row>

    <b-row class="d-flex">
      <b-col cols="3" class="flex-fill">
        <b-button
          v-b-tooltip.hover
          variant="primary"
          block
          title="Reset all filters"
          @click="onResetFilters"
        >
          <b-icon-backspace-fill />
        </b-button>
      </b-col>
      <b-col cols="3" class="flex-fill">
        <b-button
          v-b-tooltip.hover
          variant="primary"
          block
          title="Show only past trips"
          @click="onShowPastTrips"
        >
          <b-icon-archive-fill />
        </b-button>
      </b-col>
      <b-col cols="3" class="flex-fill">
        <b-button
          v-b-tooltip.hover
          variant="primary"
          block
          title="Show upcoming trips"
          @click="onShowUpcomingTrips"
        >
          <b-icon-calendar-fill />
        </b-button>
      </b-col>
      <b-col cols="3" class="flex-fill">
        <b-button
          v-b-tooltip.hover
          variant="primary"
          block
          title="Show next month trips"
          @click="onShowNextMonthTrips"
        >
          <b-icon-alarm-fill />
        </b-button>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import moment from 'moment'
import TripDestinationInput from '~/components/trips/TripDestinationInput'
import TripDateInput from '~/components/trips/TripDateInput'

export const filter = (
  destinationFilter,
  startDateStartFilter,
  startDateEndFilter,
  endDateStartFilter,
  endDateEndFilter,
  item,
  filterValue
) => {
  if (destinationFilter && !item.destination.startsWith(destinationFilter)) {
    return false
  }

  if (startDateStartFilter && item.startDate < startDateStartFilter) {
    return false
  }

  if (startDateEndFilter && item.startDate > startDateEndFilter) {
    return false
  }

  if (endDateStartFilter && item.endDate < endDateStartFilter) {
    return false
  }

  if (endDateEndFilter && item.endDate > endDateEndFilter) {
    return false
  }

  return true
}

export default {
  components: {
    TripDestinationInput,
    TripDateInput
  },
  props: {
    destinationFilter: {
      type: String,
      required: true
    },
    startDateStartFilter: {
      validator: (prop) => prop instanceof Date || prop === null,
      required: true
    },
    startDateEndFilter: {
      validator: (prop) => prop instanceof Date || prop === null,
      required: true
    },
    endDateStartFilter: {
      validator: (prop) => prop instanceof Date || prop === null,
      required: true
    },
    endDateEndFilter: {
      validator: (prop) => prop instanceof Date || prop === null,
      required: true
    }
  },
  computed: {
    currentDestinationFilter: {
      get() {
        return this.destinationFilter
      },
      set(value) {
        this.$emit('update:destinationFilter', value)

        this.updateCurrentFilterValue(
          value,
          this.currentStartDateStartFilter,
          this.currentStartDateEndFilter,
          this.currentEndDateStartFilter,
          this.currentEndDateEndFilter
        )
      }
    },
    currentStartDateStartFilter: {
      get() {
        return this.startDateStartFilter
      },
      set(value) {
        this.$emit('update:startDateStartFilter', value)

        this.updateCurrentFilterValue(
          this.currentDestinationFilter,
          value,
          this.currentStartDateEndFilter,
          this.currentEndDateStartFilter,
          this.currentEndDateEndFilter
        )
      }
    },
    currentStartDateEndFilter: {
      get() {
        return this.startDateEndFilter
      },
      set(value) {
        this.$emit('update:startDateEndFilter', value)

        this.updateCurrentFilterValue(
          this.currentDestinationFilter,
          this.currentStartDateStartFilter,
          value,
          this.currentEndDateStartFilter,
          this.currentEndDateEndFilter
        )
      }
    },
    currentEndDateStartFilter: {
      get() {
        return this.endDateStartFilter
      },
      set(value) {
        this.$emit('update:endDateStartFilter', value)

        this.updateCurrentFilterValue(
          this.currentDestinationFilter,
          this.currentStartDateStartFilter,
          this.currentStartDateEndFilter,
          value,
          this.currentEndDateEndFilter
        )
      }
    },
    currentEndDateEndFilter: {
      get() {
        return this.endDateEndFilter
      },
      set(value) {
        this.$emit('update:endDateEndFilter', value)

        this.updateCurrentFilterValue(
          this.currentDestinationFilter,
          this.currentStartDateStartFilter,
          this.currentStartDateEndFilter,
          this.currentEndDateStartFilter,
          value
        )
      }
    }
  },
  mounted() {
    this.updateCurrentFilterValue(
      this.currentDestinationFilter,
      this.currentStartDateStartFilter,
      this.currentStartDateEndFilter,
      this.currentEndDateStartFilter,
      this.currentEndDateEndFilter
    )
  },
  methods: {
    updateCurrentFilterValue(
      destinationFilter,
      startDateStartFilter,
      startDateEndFilter,
      endDateStartFilter,
      endDateEndFilter
    ) {
      const filters = [
        destinationFilter,
        startDateStartFilter,
        startDateEndFilter,
        endDateStartFilter,
        endDateEndFilter
      ]

      let filterValue = ''

      filters.forEach((filter) => {
        if (filter) {
          filterValue += filter
        }
      })

      this.$emit('update:filterValue', filterValue)
    },
    onResetFilters() {
      this.currentDestinationFilter = ''
      this.currentStartDateStartFilter = null
      this.currentStartDateEndFilter = null
      this.currentEndDateStartFilter = null
      this.currentEndDateEndFilter = null
    },
    onShowPastTrips() {
      this.currentStartDateStartFilter = null
      this.currentStartDateEndFilter = null
      this.currentEndDateStartFilter = null
      this.currentEndDateEndFilter = moment(new Date())
        .startOf('day')
        .toDate()
    },
    onShowUpcomingTrips() {
      this.currentStartDateStartFilter = moment(new Date())
        .startOf('day')
        .toDate()
      this.currentStartDateEndFilter = null
      this.currentEndDateStartFilter = null
      this.currentEndDateEndFilter = null
    },
    onShowNextMonthTrips() {
      this.currentStartDateStartFilter = moment(new Date())
        .add(1, 'months')
        .startOf('month')
        .startOf('day')
        .toDate()
      this.currentStartDateEndFilter = moment(new Date())
        .add(1, 'months')
        .endOf('month')
        .startOf('day')
        .toDate()
      this.currentEndDateStartFilter = null
      this.currentEndDateEndFilter = null
    }
  }
}
</script>
