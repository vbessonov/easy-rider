<template>
  <ValidationObserver v-slot="{ invalid, handleSubmit }">
    <b-form @submit.prevent="handleSubmit(onSubmit)" @reset.prevent="onReset">
      <b-row>
        <b-col cols="12">
          <ValidatableUserEmailInput
            v-model="currentValue.email"
            :label="'Email:'"
          />
        </b-col>
      </b-row>

      <b-row>
        <b-col cols="12">
          <ValidatableUserPasswordInput
            v-model="currentValue.password"
            :label="'Password:'"
          />
        </b-col>
      </b-row>

      <b-row>
        <b-col cols="12">
          <UserRoleSelect
            v-model="currentValue.role"
            :label="'Role:'"
            :placeholder="null"
          >
            <template v-slot:first> </template>
          </UserRoleSelect>
        </b-col>
      </b-row>

      <b-row>
        <b-col cols="12" class="text-right">
          <b-button type="reset" variant="secondary" @click="onCancel">
            Cancel
          </b-button>
          <b-button type="submit" variant="primary">
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
import ValidatableUserEmailInput from '~/components/users/ValidatableUserEmailInput'
import ValidatableUserPasswordInput from '~/components/users/ValidatableUserPasswordInput'
import UserRoleSelect from '~/components/users/UserRoleSelect'
import BaseComponentMixin from '~/components/BaseComponentMixin'

export default {
  components: {
    ValidatableUserEmailInput,
    ValidatableUserPasswordInput,
    UserRoleSelect
  },
  mixins: [BaseComponentMixin],
  props: {
    value: {
      type: Object,
      required: true
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
