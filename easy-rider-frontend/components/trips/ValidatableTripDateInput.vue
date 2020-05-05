<template>
  <ValidationProvider v-slot="validationContext" :name="name" rules="required">
    <TripDateInput
      :id="id"
      v-model="currentValue"
      :readonly="readonly"
      v-bind="$attrs"
      :placeholder="placeholder"
      :state="getValidationState(validationContext)"
    >
      <template v-slot:feedback>
        {{ validationContext.errors[0] }}
      </template>
    </TripDateInput>
  </ValidationProvider>
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
    value: {
      validator: (prop) => prop instanceof Date || prop === null,
      required: true
    },
    id: {
      type: String,
      required: true
    },
    readonly: {
      type: Boolean,
      default: false
    },
    name: {
      type: String,
      required: true
    },
    placeholder: {
      type: String,
      default: 'Date'
    }
  }
}
</script>
