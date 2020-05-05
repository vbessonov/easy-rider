<template>
  <ValidationObserver ref="observer" v-slot="{ invalid, handleSubmit }">
    <b-form @submit.prevent="handleSubmit(onSubmit)">
      <ValidatableUserEmailInput v-model="user.email" />
      <ValidatableUserPasswordInput v-model="user.password" />

      <b-button type="submit" variant="primary">
        <slot name="submit-button-content">
          Login
        </slot>
      </b-button>
    </b-form>
  </ValidationObserver>
</template>

<script>
import User from '~/models/User'
import ValidatableUserEmailInput from '~/components/users/ValidatableUserEmailInput'
import ValidatableUserPasswordInput from '~/components/users/ValidatableUserPasswordInput'

export default {
  components: {
    ValidatableUserEmailInput,
    ValidatableUserPasswordInput
  },
  data() {
    return {
      user: new User('', '')
    }
  },
  methods: {
    onSubmit() {
      this.$emit('submit', this.user)
    }
  }
}
</script>
