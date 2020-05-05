<template>
  <b-form-group id="email-input-group" label-for="email-input" v-bind="$attrs">
    <b-form-input
      id="email-input"
      v-model="currentValue"
      type="text"
      :placeholder="placeholder"
      v-bind="$attrs"
    />

    <b-form-invalid-feedback id="email-input-feedback">
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
      default: 'Email Address'
    }
  }
}
</script>
