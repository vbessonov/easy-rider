<template>
  <b-form-group :id="`${id}-group`" :label-for="id" v-bind="$attrs">
    <b-form-datepicker
      :id="id"
      v-model="currentValue"
      :placeholder="placeholder"
      v-bind="labels[locale] || {}"
      :locale="locale"
      :start-weekday="weekday"
      :value-as-date="true"
      :disabled="readonly"
      :date-format-options="{
        year: 'numeric',
        month: 'numeric',
        day: 'numeric'
      }"
    />

    <b-form-invalid-feedback :id="`${id}-feedback`">
      <slot name="feedback"></slot>
    </b-form-invalid-feedback>
  </b-form-group>
</template>

<script>
import { mapState } from 'vuex'
import BaseComponentMixin from '~/components/BaseComponentMixin'

export default {
  mixins: [BaseComponentMixin],
  inheritAttrs: false,
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
    placeholder: {
      type: String,
      required: false,
      default: 'Date'
    }
  },
  computed: {
    ...mapState('account', ['locale', 'locales', 'weekday', 'labels'])
  }
}
</script>
