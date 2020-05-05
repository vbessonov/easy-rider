<template>
  <div></div>
</template>

<script>
export default {
  layout: 'simple',
  async mounted() {
    await this.$auth.logout()

    this.$router.replace('/account/signin')
  },
  head() {
    return {
      title: 'Easy Rider | Logout'
    }
  }
}
</script>
