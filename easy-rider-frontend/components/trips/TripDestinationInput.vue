<template>
  <b-form-group
    id="destination-input-group"
    label-for="destination-input"
    v-bind="$attrs"
  >
    <b-form-input
      id="destination-input"
      v-model="currentValue"
      type="text"
      :placeholder="placeholder"
      v-bind="$attrs"
    />

    <b-form-invalid-feedback id="destination-input-feedback">
      <slot name="feedback"></slot>
    </b-form-invalid-feedback>
  </b-form-group>
</template>

<script>
import BaseComponentMixin from '~/components/BaseComponentMixin'

export default {
  mixins: [BaseComponentMixin],
  props: {
    placeholder: {
      type: String,
      default: 'Destination'
    }
  }
}
</script>
