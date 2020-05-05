<template>
  <Table
    ref="table"
    :fields="fields"
    :items="users"
    :busy="busy"
    :filter-function="filter"
    :filter="filters.filterValue"
    @filtered="onFiltered"
    v-on="$listeners"
  >
    <template v-slot:filter>
      <UserFilterForm v-bind.sync="filters" />
    </template>

    <template v-slot:cell(email)="row">
      <b-link :to="`/users/${row.item.id}`">
        {{ row.item.email }}
      </b-link>
    </template>
  </Table>
</template>

<script>
import { ROLES } from '~/models/Roles'
import Table from '~/components/Table'
import UserFilterForm, {
  filter as userFilterFormFilter
} from '~/components/users/UserFilterForm'

export default {
  components: {
    Table,
    UserFilterForm
  },
  props: {
    users: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      fields: [
        { key: 'email', label: 'Email', sortable: true },
        {
          key: 'role',
          label: 'Role',
          formatter: (value, key, item) => {
            if (item) {
              return ROLES[item.role]
            } else {
              return ''
            }
          },
          sortable: true,
          sortByFormatted: true,
          filterByFormatted: true,
          thStyle: {
            width: '10rem'
          }
        }
      ],
      filters: {
        emailFilter: '',
        roleFilter: 0,
        filterValue: null
      },
      busy: false
    }
  },
  methods: {
    filter(item, filterValue) {
      // if (!this.busy) {
      //   this.busy = true
      // }

      return userFilterFormFilter(
        this.filters.emailFilter,
        this.filters.roleFilter,
        item,
        filterValue
      )
    },
    onFiltered() {
      // this.busy = false
    }
  }
}
</script>
