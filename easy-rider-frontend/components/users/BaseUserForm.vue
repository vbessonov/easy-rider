<template>
  <b-container>
    <b-form v-bind="$attrs" v-on="$listeners">
      <b-form-group id="email-input-group">
        <b-form-input
          id="email-input"
          v-model="currentUser.email"
          type="email"
          required
          placeholder="Email Address"
          @input="$emit('update:email', $event.target.value)"
        />
      </b-form-group>

      <b-form-group id="password-input-group">
        <b-form-input
          id="password-input"
          v-model="currentUser.password"
          type="password"
          required
          placeholder="Password"
          @input="$emit('update:password', $event.target.value)"
        ></b-form-input>
      </b-form-group>

      <slot name="additional-controls"></slot>

      <b-button type="submit" variant="primary">
        <slot name="submit-buttton-content">
          Submit
        </slot>
      </b-button>

      <slot name="reset-button">
        <b-button type="reset" variant="secondary">
          Cancel
        </b-button>
      </slot>
    </b-form>
  </b-container>
</template>

<script>
import User from '~/models/User'

export default {
  props: {
    user: {
      type: User,
      required: true
    }
  },
  data() {
    return {
      currentUser: this.user
    }
  }
}
</script>
