<template>
  <div class="d-flex justify-content-center">
    <b-row>
      <b-col
        sm="auto"
        class="d-flex flex-column justify-content-center align-items-center text-center"
      >
        <Alert :error="error" />

        <Logo />

        <UserLoginForm v-on="$listeners">
          <template v-for="(_, slot) of $scopedSlots" v-slot:[slot]="scope">
            <slot :name="slot" v-bind="scope" />
          </template>
        </UserLoginForm>

        <slot name="additional-controls"> </slot>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import Alert from '~/components/Alert'
import Logo from '~/components/Logo'
import UserLoginForm from '~/components/users/UserLoginForm'

export default {
  auth: 'guest',
  layout: 'simple',
  components: {
    Alert,
    Logo,
    UserLoginForm
  },
  props: {
    error: {
      type: Error,
      required: false,
      default: null
    }
  }
}
</script>
