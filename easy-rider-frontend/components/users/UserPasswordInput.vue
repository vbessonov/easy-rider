<template>
  <b-form-group
    id="password-input-group"
    label-for="password-input"
    v-bind="$attrs"
  >
    <b-form-input
      id="password-input"
      v-model="currentValue"
      type="password"
      :placeholder="placeholder"
      v-bind="$attrs"
    />
    <b-form-invalid-feedback id="password-input-feedback">
      <slot name="feedback"> </slot>
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
      default: 'Password'
    }
  }
}
</script>
