<template>
  <b-form-group id="role-input-group" label-for="role-select" v-bind="$attrs">
    <b-form-select
      id="role-select"
      v-model="currentValue"
      :options="availableRoleOptions"
      :disabled="!availableRoleOptions || availableRoleOptions.length == 0"
      v-bind="$attrs"
    >
      <template v-if="placeholder" v-slot:first>
        <b-form-select-option :value="0" class="first-option">
          {{ placeholder }}
        </b-form-select-option>
      </template>
    </b-form-select>

    <b-form-invalid-feedback id="role-input-feedback">
      <slot name="feedback"></slot>
    </b-form-invalid-feedback>
  </b-form-group>
</template>

<script>
import { mapGetters } from 'vuex'
import BaseComponentMixin from '~/components/BaseComponentMixin'

export default {
  mixins: [BaseComponentMixin],
  props: {
    value: {
      type: Number,
      required: true
    },
    placeholder: {
      type: String,
      required: false,
      default: '-- Please select an option --'
    }
  },
  computed: {
    ...mapGetters('account', ['availableRoleOptions'])
  }
}
</script>

<style>
.first-option {
  color: #6c757c;
}
</style>
