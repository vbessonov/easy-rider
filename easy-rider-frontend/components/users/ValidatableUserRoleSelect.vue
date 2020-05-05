<template>
  <ValidationProvider v-slot="validationContext" name="Role" rules="required">
    <UserRoleSelect
      v-model="currentValue"
      v-bind="$attrs"
      :placeholder="placeholder"
      :state="getValidationState(validationContext)"
    >
      <template v-slot:feedback>
        {{ validationContext.errors[0] }}
      </template>
    </UserRoleSelect>
  </ValidationProvider>
</template>

<script>
import BaseComponentMixin from '~/components/BaseComponentMixin'
import UserRoleSelect from '~/components/users/UserRoleSelect'

export default {
  components: {
    UserRoleSelect
  },
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
  }
}
</script>
