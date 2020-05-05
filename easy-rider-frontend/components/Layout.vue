<template>
  <div class="page">
    <header>
      <slot name="header">
        <NavigationBar />
        <Breadcrumb />
      </slot>
    </header>
    <nuxt class="content" />
    <footer>
      <p>&copy; 2020, Hilbert Team, Inc.</p>
    </footer>
  </div>
</template>

<script>
import NavigationBar from '~/components/NavigationBar'
import Breadcrumb from '~/components/Breadcrumb'

export default {
  components: {
    NavigationBar,
    Breadcrumb
  }
}
</script>

<style>
.page {
  display: flex;
  min-height: 100vh;
  flex-direction: column;
}

.content {
  flex: 1;
}

footer {
  border-top: 1px solid #eee;
  text-align: center;
}

footer p {
  color: #595959;
  font-size: 12px;
  font-weight: 400;
  line-height: 1.5;
}
</style>
