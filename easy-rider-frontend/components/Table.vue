<template>
  <b-container class="p-0">
    <b-row v-show="filterable">
      <b-col cols="12">
        <slot name="filter"></slot>
      </b-col>
    </b-row>

    <b-row v-if="!readonly" class="mb-1">
      <b-col cols="12">
        <b-button
          v-b-tooltip.hover
          variant="primary"
          block
          title="Add a new item"
          @click="onAdd"
        >
          <b-icon-plus-circle-fill />
        </b-button>
      </b-col>
    </b-row>

    <b-row>
      <b-col cols="12">
        <b-table
          ref="table"
          striped
          hover
          show-empty
          sort-icon-left
          primary-key="id"
          :fields="fields"
          :items="items"
          :current-page="currentPage"
          :per-page="rowsPerPage"
          v-bind="$attrs"
          @filtered="onFiltered"
          v-on="$listeners"
        >
          <slot name="table-busy">
            <div slot="table-busy" class="text-center my-3">
              <b-spinner class="align-middle" />
            </div>
          </slot>

          <template v-if="!readonly" v-slot:cell(actions)="row">
            <b-button
              v-b-tooltip.hover
              variant="primary"
              title="Edit item"
              @click="onEdit(row.index, row.item)"
            >
              <b-icon-pencil-square />
            </b-button>
            <b-button
              v-b-tooltip.hover
              variant="primary"
              title="Delete item"
              @click="onDelete(row.index, row.item)"
            >
              <b-icon-trash-fill />
            </b-button>
          </template>

          <template v-for="(_, slot) of $scopedSlots" v-slot:[slot]="scope">
            <slot :name="slot" v-bind="scope" />
          </template>
        </b-table>
      </b-col>
    </b-row>

    <b-row v-if="pagination">
      <b-col cols="12">
        <b-pagination
          v-model="currentPage"
          :total-rows="totalRows"
          :per-page="rowsPerPage"
          class="justify-content-md-center"
        />
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import { mapState } from 'vuex'

export default {
  props: {
    items: {
      type: Array,
      required: true
    },
    fields: {
      type: Array,
      required: true
    },
    filterable: {
      type: Boolean,
      default: true
    },
    readonly: {
      type: Boolean,
      default: false
    },
    pagination: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      totalRows: 1,
      currentPage: 1
    }
  },
  computed: {
    ...mapState('account', ['pagingOptions']),
    rowsPerPage() {
      if (this.pagination) {
        return this.$store.state.account.rowsPerPage
      }

      return 0
    }
  },
  mounted() {
    this.totalRows = this.items.length

    if (!this.readonly) {
      this.fields.push({
        key: 'actions',
        label: 'Actions',
        sortable: false,
        thStyle: {
          width: '10rem'
        }
      })
    }
  },
  methods: {
    onFiltered(filteredItems) {
      this.totalRows = filteredItems.length
      this.currentPage = 1
    },
    onAdd(index, item) {
      this.$emit('add')
    },
    onEdit(index, item) {
      this.$emit('edit', item)
    },
    onDelete(index, item) {
      this.$emit('delete', item)
    }
  }
}
</script>
