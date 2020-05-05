<template>
  <div>
    <UserEmailInput
      v-model="currentEmailFilter"
      placeholder="Start typing to filter users by an email address"
    />
    <UserRoleSelect
      v-model="currentRoleFilter"
      placeholder="Select an option to filter users by a role"
    />
  </div>
</template>

<script>
import UserEmailInput from './UserEmailInput'
import UserRoleSelect from './UserRoleSelect'

export const filter = (emailFilter, roleFilter, item, filterValue) => {
  if (emailFilter && !item.email.startsWith(emailFilter)) {
    return false
  }

  if (roleFilter && item.role !== parseInt(roleFilter)) {
    return false
  }

  return true
}

export default {
  components: {
    UserEmailInput,
    UserRoleSelect
  },
  props: {
    emailFilter: {
      type: String,
      required: true
    },
    roleFilter: {
      type: Number,
      required: true
    }
  },
  computed: {
    currentEmailFilter: {
      get() {
        return this.emailFilter
      },
      set(value) {
        this.$emit('update:emailFilter', value)
        this.updateCurrentFilterValue(value, this.currentRoleFilter)
      }
    },
    currentRoleFilter: {
      get() {
        return this.roleFilter
      },
      set(value) {
        this.$emit('update:roleFilter', value)
        this.updateCurrentFilterValue(this.currentEmailFilter, value)
      }
    }
  },
  methods: {
    updateCurrentFilterValue(emailFilter, roleFilter) {
      let filterValue = ''

      if (emailFilter) {
        filterValue += emailFilter
      }
      if (roleFilter !== 0) {
        filterValue += roleFilter
      }

      this.$emit('update:filterValue', filterValue)
    }
  }
}
</script>
