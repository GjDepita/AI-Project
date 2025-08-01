import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      // Enables @ as src shortcut
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      // Enables Vue template compiler
      'vue': 'vue/dist/vue.esm-bundler.js',
    },
  },
})
