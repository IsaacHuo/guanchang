import { defineNuxtConfig } from 'nuxt/config'

export default defineNuxtConfig({
  modules: [
    '@nuxtjs/tailwindcss'
  ],
  devServer: {
    port: 3333
  },
  css: ['~/assets/css/main.css'],
  compatibilityDate: '2024-04-03',
})