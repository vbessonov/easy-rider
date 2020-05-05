<template>
  <b-form-group
    id="destination-input-group"
    label-for="destination-input"
    v-bind="$attrs"
  >
    <b-textarea
      id="destination-input"
      v-model="currentValue"
      :placeholder="placeholder"
      v-bind="$attrs"
    />
  </b-form-group>
</template>

<script>
import BaseComponentMixin from '~/components/BaseComponentMixin'

export default {
  mixins: [BaseComponentMixin],
  props: {
    placeholder: {
      type: String,
      default: 'Place your comment here...'
    }
  }
}
</script>
