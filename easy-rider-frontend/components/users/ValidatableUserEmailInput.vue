<template>
  <ValidationProvider
    v-slot="validationContext"
    name="Email"
    rules="required|email"
  >
    <UserEmailInput
      v-model="currentValue"
      v-bind="$attrs"
      :placeholder="placeholder"
      :state="getValidationState(validationContext)"
    >
      <template v-slot:feedback>
        {{ validationContext.errors[0] }}
      </template>
    </UserEmailInput>
  </ValidationProvider>
</template>

<script>
import BaseComponentMixin from '~/components/BaseComponentMixin'
import UserEmailInput from '~/components/users/UserEmailInput'

export default {
  components: {
    UserEmailInput
  },
  mixins: [BaseComponentMixin],
  props: {
    placeholder: {
      type: String,
      default: 'Email Address'
    }
  }
}
</script>
