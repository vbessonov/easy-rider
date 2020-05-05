<template>
  <ValidationProvider
    v-slot="validationContext"
    name="Destination"
    rules="required"
  >
    <TripDestinationInput
      v-model="currentValue"
      v-bind="$attrs"
      :placeholder="placeholder"
      :state="getValidationState(validationContext)"
    >
      <template v-slot:feedback>
        {{ validationContext.errors[0] }}
      </template>
    </TripDestinationInput>
  </ValidationProvider>
</template>

<script>
import BaseComponentMixin from '~/components/BaseComponentMixin'
import TripDestinationInput from '~/components/trips/TripDestinationInput'

export default {
  components: {
    TripDestinationInput
  },
  mixins: [BaseComponentMixin],
  props: {
    placeholder: {
      type: String,
      default: 'Destination'
    }
  }
}
</script>
