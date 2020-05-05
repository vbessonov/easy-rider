import Vue from 'vue'

const DUMMY_PASSWORD = 'dummy'

export const state = () => ({
  users: {}
})

export const getters = {
  userList(state, getters, rootState) {
    return Object.values(state.users).filter((user) => {
      if (parseInt(user.id) === rootState.auth.user.id) {
        return false
      }
      if (user.role > rootState.auth.user.role) {
        return false
      }

      return true
    })
  }
}

export const mutations = {
  add(state, users) {
    users.forEach((user) => {
      Vue.set(state.users, user.id, user)
    })
  },
  update(state, user) {
    Vue.set(state.users, user.id, user)
  },
  remove(state, user) {
    Vue.delete(state.users, user.id)
  },
  clear(state) {
    state.users = {}
  }
}

export const actions = {
  async list(context) {
    const users = await this.$axios.$get('/users/')

    users.forEach((user) => {
      user.password = DUMMY_PASSWORD
    })

    context.commit('add', users)

    return users
  },
  async retrieve(context, userId) {
    let user = null

    if (userId in context.state.users) {
      user = context.state.users[userId]
    } else {
      user = await this.$axios.$get(`/users/${userId}/`)
      user.password = DUMMY_PASSWORD

      context.commit('add', [user])
    }

    return user
  },
  async create(context, user) {
    const createdUser = await this.$axios.$post('/users/', user)
    createdUser.password = DUMMY_PASSWORD

    context.commit('add', [createdUser])

    return createdUser
  },
  async update(context, user) {
    if (user.password === DUMMY_PASSWORD) {
      await this.$axios.$patch(`/users/${user.id}/`, {
        email: user.email,
        role: user.role
      })
    } else {
      await this.$axios.$put(`/users/${user.id}/`, user)
    }

    context.commit('update', user)
  },
  async destroy(context, user) {
    await this.$axios.$delete(`/users/${user.id}/`)

    context.commit('remove', user)
  },
  clear(context) {
    context.commit('clear')
  }
}
