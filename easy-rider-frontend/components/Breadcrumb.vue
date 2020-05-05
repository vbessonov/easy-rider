<template>
  <b-breadcrumb v-if="items && items.length > 1" :items="items"></b-breadcrumb>
</template>

<script>
import { mapState, mapGetters } from 'vuex'
import _ from 'lodash'

export default {
  computed: {
    ...mapState('users', ['users']),
    ...mapState('auth', ['user']),
    ...mapGetters('account', ['isPrivileged']),
    items() {
      const params = this.$route.params
      const path = _.trimStart(this.$route.matched[0].path, '/')
      const pathItems = path.split('/')
      let breadcrumbItems = [
        {
          text: 'Home',
          to: '/'
        }
      ]

      if (this.isPrivileged) {
        breadcrumbItems = breadcrumbItems.concat(
          this.getBreadcrumbItemsForPrivilegedUser(pathItems, params)
        )
      } else {
        breadcrumbItems = breadcrumbItems.concat(
          this.getBreadcrumbItemsForUnprivilegedUser(pathItems, params)
        )
      }

      return breadcrumbItems
    }
  },
  methods: {
    getBreadcrumbItemsForPrivilegedUser(pathItems, params) {
      const breadcrumbItems = []

      pathItems.forEach((pathItem) => {
        switch (pathItem) {
          case 'users': {
            breadcrumbItems.push({
              text: 'Users',
              to: '/users'
            })
            break
          }

          case 'add': {
            if (!_.includes(pathItems, ':userId')) {
              breadcrumbItems.push({
                text: 'New user',
                to: '/users/add'
              })
            } else {
              const userId = params.userId

              breadcrumbItems.push({
                text: 'New trip',
                to: `/users/${userId}/trips/add`
              })
            }
            break
          }

          case ':userId': {
            const userId = params.userId

            breadcrumbItems.push({
              text: this.getUserBreadcrumbText(userId),
              to: `/users/${userId}`
            })
            break
          }

          case ':trips': {
            const userId = params.userId

            breadcrumbItems.push({
              text: 'Trips',
              to: `/users/${userId}/trips`
            })
            break
          }

          case ':tripId': {
            const userId = params.userId
            const tripId = params.tripId

            breadcrumbItems.push({
              text: this.getTripBreadcrumbText(userId),
              to: `/users/${userId}/trips/${tripId}`
            })
            break
          }

          case 'itinerary': {
            const userId = params.userId

            breadcrumbItems.push({
              text: 'Itinerary',
              to: `/users/${userId}/trips/print`
            })
            break
          }
        }
      })

      return breadcrumbItems
    },
    getBreadcrumbItemsForUnprivilegedUser(pathItems, params) {
      const breadcrumbItems = []

      pathItems.forEach((pathItem) => {
        switch (pathItem) {
          case ':trips': {
            const userId = params.userId

            breadcrumbItems.push({
              text: 'My Trips',
              to: `/users/${userId}/trips`
            })
            break
          }

          case ':tripId': {
            const userId = params.userId
            const tripId = params.tripId

            breadcrumbItems.push({
              text: this.getTripBreadcrumbText(userId),
              to: `/users/${userId}/trips/${tripId}`
            })
            break
          }

          case 'itinerary': {
            const userId = params.userId

            breadcrumbItems.push({
              text: 'Itinerary',
              to: `/users/${userId}/trips/print`
            })
            break
          }
        }
      })

      return breadcrumbItems
    },
    getUserBreadcrumbText(userId) {
      return `User # ${userId}`
    },
    getTripBreadcrumbText(tripId) {
      return `Trip # ${tripId}`
    }
  }
}
</script>
