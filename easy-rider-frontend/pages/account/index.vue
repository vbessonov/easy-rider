<template>
  <b-container fluid>
    <h3>Your profile</h3>

    <b-form-group label="Email:" label-for="email-input">
      <b-form-input id="email-input" type="text" readonly :value="user.email" />
    </b-form-group>

    <b-form-group label="Locale:" label-for="locales-select">
      <b-form-select id="locales-select" v-model="locale" :options="locales" />
    </b-form-group>

    <b-form-group label="Start weekday:" label-for="start-weekday-select">
      <b-form-select
        id="start-weekday-select"
        v-model="weekday"
        :options="weekdays"
      ></b-form-select>
    </b-form-group>

    <b-form-group label="Rows per page:" label-for="rowsPerPageSelect">
      <b-form-select
        id="rowsPerPageSelect"
        v-model="rowsPerPage"
        :options="pagingOptions"
      />
    </b-form-group>
  </b-container>
</template>

<script>
import { mapState } from 'vuex'

export default {
  computed: {
    ...mapState('auth', ['user']),
    ...mapState('account', ['locales', 'weekdays', 'pagingOptions']),
    locale: {
      get() {
        return this.$store.state.account.locale
      },
      set(value) {
        this.$store.commit('account/setLocale', value)
      }
    },
    weekday: {
      get() {
        return this.$store.state.account.weekday
      },
      set(value) {
        this.$store.commit('account/setWeekday', value)
      }
    },
    rowsPerPage: {
      get() {
        return this.$store.state.account.rowsPerPage
      },
      set(value) {
        this.$store.commit('account/setRowsPerPage', value)
      }
    }
  },
  head() {
    return {
      title: 'Easy Rider | Account'
    }
  }
}
</script>
