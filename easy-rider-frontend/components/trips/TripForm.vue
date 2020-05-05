<template>
  <b-container>
    <b-form @submit.prevent="onSubmit">
      <b-form-group id="destination-input-group">
        <b-form-input
          id="destination-input"
          v-model="trip.destination"
          type="text"
          required
          placeholder="Destination"
        />
      </b-form-group>

      <b-form-group id="start-date-input-group">
        <b-form-input
          id="start-date-input"
          v-model="trip.startDate"
          type="date"
          required
        />
      </b-form-group>

      <b-form-group id="end-date-input-group">
        <b-form-input
          id="end-date-input"
          v-model="trip.endDate"
          type="date"
          required
        />
      </b-form-group>

      <b-form-group id="comment-input-group">
        <b-form-input
          id="comment-input"
          v-model="trip.comment"
          type="text"
          required
        />
      </b-form-group>

      <b-button type="submit" variant="primary">
        {{ submitButtonTitle }}
      </b-button>
    </b-form>
  </b-container>
</template>

<script>
import Trip from '~/models/Trip'

export default {
  props: {
    trip: {
      type: Trip,
      default: () => new Trip('', '', '', '')
    },
    submitButtonTitle: {
      type: String,
      default: 'Add'
    }
  },
  methods: {
    onSubmit() {
      this.$emit('submit', this.trip)
    }
  }
}
</script>
