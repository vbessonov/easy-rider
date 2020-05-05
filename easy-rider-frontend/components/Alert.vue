<template>
  <b-alert
    v-if="errorMessage != null"
    :show="errorMessage != null"
    dismissible
    variant="danger"
  >
    {{ errorMessage }}
  </b-alert>
</template>

<script>
export default {
  props: {
    error: {
      type: Error,
      required: false,
      default: null
    }
  },
  computed: {
    errorMessage() {
      if (!this.error) {
        return null
      }

      const response = this.error.response

      if (response != null && response.data != null) {
        const messages = Object.values(response.data)

        return this.capitalize(this.unwrap(messages))
      }

      if (this.error.message.includes('network')) {
        return 'Remote server did not respond in time. Please try again later'
      }

      return this.error.message
    }
  },
  methods: {
    unwrap(value) {
      if (Array.isArray(value)) {
        return this.unwrap(value[0])
      }

      return value
    },
    capitalize(string) {
      return string[0].toUpperCase() + string.slice(1)
    }
  }
}
</script>
