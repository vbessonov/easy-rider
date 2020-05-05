<template>
  <ValidationProvider
    v-slot="validationContext"
    name="Password"
    rules="required"
  >
    <UserPasswordInput
      v-model="currentValue"
      v-bind="$attrs"
      :placeholder="placeholder"
      :state="getValidationState(validationContext)"
    >
      <template v-slot:feedback>
        {{ validationContext.errors[0] }}
      </template>
    </UserPasswordInput>
  </ValidationProvider>
</template>

<script>
import BaseComponentMixin from '~/components/BaseComponentMixin'
import UserPasswordInput from '~/components/users/UserPasswordInput'

export default {
  components: {
    UserPasswordInput
  },
  mixins: [BaseComponentMixin],
  props: {
    placeholder: {
      type: String,
      default: 'Password'
    }
  }
}
</script>
