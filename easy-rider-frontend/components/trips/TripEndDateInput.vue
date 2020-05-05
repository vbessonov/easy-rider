<template>
  <TripDateInput
    id="end-date-input"
    v-model="currentValue"
    :placeholder="placeholder"
  />
</template>

<script>
import BaseComponentMixin from '~/components/BaseComponentMixin'
import TripDateInput from '~/components/trips/TripDateInput'

export default {
  components: {
    TripDateInput
  },
  mixins: [BaseComponentMixin],
  props: {
    placeholder: {
      type: String,
      default: 'End Date'
    }
  }
}
</script>
