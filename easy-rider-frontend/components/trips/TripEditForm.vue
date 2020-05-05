<template>
  <ValidationObserver v-slot="{ invalid, handleSubmit }">
    <b-form @submit.prevent="handleSubmit(onSubmit)" @reset.prevent="onReset">
      <b-row>
        <b-col cols="12">
          <ValidatableTripDestinationInput
            v-model="currentValue.destination"
            :disabled="readonly"
            label="Destination:"
          />
        </b-col>
      </b-row>

      <b-row>
        <b-col cols="12">
          <ValidatableTripStartDateInput
            v-model="currentValue.startDate"
            :trip="currentValue"
            :readonly="readonly"
            label="Start date:"
          />
        </b-col>
      </b-row>

      <b-row>
        <b-col cols="12">
          <ValidatableTripEndDateInput
            v-model="currentValue.endDate"
            :trip="currentValue"
            :readonly="readonly"
            label="End date:"
          />
        </b-col>
      </b-row>

      <b-row>
        <b-col cols="12">
          <TripCommentInput
            v-model="currentValue.comment"
            :disabled="readonly"
            label="Comment:"
          />
        </b-col>
      </b-row>

      <b-row>
        <b-col cols="12" class="text-right">
          <b-button type="reset" variant="secondary" @click="onCancel">
            Cancel
          </b-button>
          <b-button type="submit" variant="primary" :disabled="readonly">
            <slot name="submit-button-content">
              Create
            </slot>
          </b-button>
        </b-col>
      </b-row>
    </b-form>
  </ValidationObserver>
</template>

<script>
import ValidatableTripDestinationInput from '~/components/trips/ValidatableTripDestinationInput'
import ValidatableTripStartDateInput from '~/components/trips/ValidatableTripStartDateInput'
import ValidatableTripEndDateInput from '~/components/trips/ValidatableTripEndDateInput'
import TripCommentInput from '~/components/trips/TripCommentInput'
import BaseComponentMixin from '~/components/BaseComponentMixin'

export default {
  components: {
    ValidatableTripDestinationInput,
    ValidatableTripStartDateInput,
    ValidatableTripEndDateInput,
    TripCommentInput
  },
  mixins: [BaseComponentMixin],
  props: {
    value: {
      type: Object,
      required: true
    },
    readonly: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    onSubmit() {
      this.$emit('submit', this.value)
    },
    onReset() {},
    onCancel() {
      this.$emit('cancel')
    }
  }
}
</script>
