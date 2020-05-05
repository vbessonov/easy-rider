export default {
  props: {
    value: {
      type: String,
      required: false
    }
  },
  computed: {
    currentValue: {
      get() {
        return this.value
      },
      set(value) {
        this.$emit('input', value)
      }
    }
  },
  methods: {
    getValidationState({ dirty, validated, valid = null }) {
      return dirty || validated ? valid : null
    }
  }
}
