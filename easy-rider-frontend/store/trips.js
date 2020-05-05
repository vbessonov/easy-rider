import Vue from 'vue'
import { dateToString } from '~/utils/date'

export const state = () => ({
  trips: {}
})

export const getters = {
  tripList(state) {
    return (userId) =>
      userId in state.trips ? Object.values(state.trips[userId]) : []
  }
}

export const mutations = {
  add(state, { userId, trips }) {
    let tripsMap = state.trips[parseInt(userId)]

    if (!tripsMap) {
      tripsMap = {}
    }

    trips.forEach((trip) => {
      trip.startDate = new Date(trip.startDate)
      trip.endDate = new Date(trip.endDate)

      tripsMap[parseInt(trip.id)] = trip
    })

    Vue.set(state.trips, userId, tripsMap)
  },
  update(state, { userId, trip }) {
    const tripsMap = state.trips[parseInt(userId)]

    trip.startDate = new Date(trip.startDate)
    trip.endDate = new Date(trip.endDate)

    Vue.set(tripsMap, parseInt(trip.id), trip)
  },
  remove(state, { userId, tripId }) {
    const tripsMap = state.trips[parseInt(userId)]

    Vue.delete(tripsMap, parseInt(tripId))
  },
  clear(state) {
    state.trips = {}
  }
}

export const actions = {
  async list(context, userId) {
    let trips = await this.$axios.$get(`/users/${userId}/trips/`)

    if (trips) {
      context.commit('add', { userId, trips })
    } else {
      trips = []
    }

    return trips
  },
  async retrieve(context, { userId, tripId }) {
    const tripsMap = context.state.trips[parseInt(userId)]
    let trip = null

    if (tripsMap && tripId in tripsMap) {
      trip = tripsMap[parseInt(tripId)]
    } else {
      trip = await this.$axios.$get(`/users/${userId}/trips/${tripId}`)

      context.commit('add', { userId, trips: [trip] })
    }

    return trip
  },
  async create(context, { userId, trip }) {
    trip.user = parseInt(userId)

    const createdTrip = await this.$axios.$post(`/users/${trip.user}/trips/`, {
      user: trip.user,
      destination: trip.destination,
      startDate: dateToString(trip.startDate),
      endDate: dateToString(trip.endDate),
      comment: trip.comment
    })

    context.commit('add', { userId, trips: [createdTrip] })

    return createdTrip
  },
  async update(context, { userId, trip }) {
    await this.$axios.$patch(`/users/${userId}/trips/${trip.id}/`, {
      user: trip.userId,
      destination: trip.destination,
      startDate: dateToString(trip.startDate),
      endDate: dateToString(trip.endDate),
      comment: trip.comment
    })

    context.commit('update', { userId, trip })
  },
  async destroy(context, { userId, tripId }) {
    await this.$axios.$delete(`/users/${userId}/trips/${tripId}/`)

    context.commit('remove', { userId, tripId })
  },
  clear(context) {
    context.commit('clear')
  }
}
