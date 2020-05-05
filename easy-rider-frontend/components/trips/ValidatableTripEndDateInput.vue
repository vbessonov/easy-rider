<template>
  <ValidatableTripDateInput
    id="end-date-input"
    v-model="currentValue"
    :readonly="readonly"
    :name="placeholder"
    :placeholder="placeholder"
  />
</template>

<script>
import BaseComponentMixin from '~/components/BaseComponentMixin'
import ValidatableTripDateInput from '~/components/trips/ValidatableTripDateInput'

export default {
  components: {
    ValidatableTripDateInput
  },
  mixins: [BaseComponentMixin],
  props: {
    value: {
      validator: (prop) => prop instanceof Date || prop === null,
      required: true
    },
    readonly: {
      type: Boolean,
      default: false
    },
    trip: {
      type: Object,
      required: true
    },
    placeholder: {
      type: String,
      default: 'End date'
    }
  }
}
</script>
