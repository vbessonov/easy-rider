<template>
  <b-navbar toggleable="lg" type="light" variant="light">
    <b-navbar-brand to="/">
      <img src="/images/logo.png" alt="Logo" />
    </b-navbar-brand>

    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>
      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">
        <!-- <b-nav-item-dropdown text="Lang" right>
          <b-dropdown-item href="#">EN</b-dropdown-item>
          <b-dropdown-item href="#">ES</b-dropdown-item>
          <b-dropdown-item href="#">RU</b-dropdown-item>
          <b-dropdown-item href="#">FA</b-dropdown-item>
        </b-nav-item-dropdown> -->

        <b-nav-item v-if="isPrivileged" to="/users">
          Users
        </b-nav-item>

        <b-nav-item v-if="user" :to="`/users/${user.id}/trips`">
          My Trips
        </b-nav-item>

        <b-nav-item-dropdown v-if="loggedIn" right>
          <template v-slot:button-content>
            <em>{{ user.email }}</em>
          </template>
          <b-dropdown-item to="/account">Account</b-dropdown-item>
          <b-dropdown-item href="#" @click="singOut">Sign Out</b-dropdown-item>
        </b-nav-item-dropdown>

        <b-nav-item v-if="!loggedIn" to="/account/signin">
          Sign In
        </b-nav-item>

        <b-nav-item
          v-if="!loggedIn"
          to="/account/signup"
          class="border border-primary border-5"
        >
          Sign Up
        </b-nav-item>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>

<script>
import { mapState, mapGetters } from 'vuex'

export default {
  computed: {
    ...mapState('auth', ['user', 'loggedIn']),
    ...mapGetters('account', ['isPrivileged'])
  },
  methods: {
    singOut() {
      this.$auth.logout()
    }
  }
}
</script>
