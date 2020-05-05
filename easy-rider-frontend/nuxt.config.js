export default {
  mode: 'universal',
  /*
   ** Headers of the page
   */
  head: {
    title: process.env.npm_package_name || '',
    meta: [
      {
        charset: 'utf-8'
      },
      {
        name: 'viewport',
        content: 'width=device-width, initial-scale=1'
      },
      {
        hid: 'description',
        name: 'description',
        content: process.env.npm_package_description || ''
      }
    ],
    link: [
      {
        rel: 'icon',
        type: 'image/x-icon',
        href: '/favicon.ico'
      }
    ]
  },
  /*
   ** Customize the progress-bar color
   */
  loading: {
    color: '#fff'
  },
  /*
   ** Global CSS
   */
  css: [],
  /*
   ** Plugins to load before mounting the App
   */
  plugins: [
    '~/plugins/VeeValidate.js',
    '~/plugins/axios.js',
    '~/plugins/vue-print-nb.js'
    // { src: '~/plugins/VuexPersistedState.js', ssr: false }
  ],
  /*
   ** Nuxt.js dev-modules
   */
  buildModules: [
    // Doc: https://github.com/nuxt-community/eslint-module
    '@nuxtjs/eslint-module'
  ],
  /*
   ** Nuxt.js modules
   */
  modules: [
    // Doc: https://bootstrap-vue.js.org
    'bootstrap-vue/nuxt',
    // Doc: https://axios.nuxtjs.org/usage
    '@nuxtjs/axios',
    '@nuxtjs/pwa',
    '@nuxtjs/auth'
  ],
  bootstrapVue: {
    icons: true
  },
  /*
   ** Router configuration
   */
  router: {
    middleware: ['auth']
  },
  /*
   ** Axios module configuration
   ** See https://axios.nuxtjs.org/options
   */
  axios: {
    baseURL: 'http://localhost:8000/api'
  },
  /*
   ** Build configuration
   */
  build: {
    /*
     ** Add an exception
     */
    transpile: ['vee-validate/dist/rules'],
    /*
     ** You can extend webpack config here
     */
    extend(config, ctx) {}
  },
  /*
   ** Authentication configuration
   */
  auth: {
    strategies: {
      local: {
        endpoints: {
          login: {
            url: '/auth/obtain_token/',
            method: 'post',
            propertyName: 'token'
          },
          logout: {
            url: '/auth/logout/',
            method: 'post'
          },
          user: {
            url: '/auth/user',
            method: 'get',
            propertyName: false
          }
        }
      }
    },
    rewriteRedirects: true,
    redirect: {
      login: '/account/signin',
      logout: '/',
      callback: '/account/signin',
      home: '/'
    }
  }
}
