import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 3000,
    allowedHosts: ['.ngrok-free.app', 'sportpredict_frontend', 'bore.pub', 'localhost', '127.0.0.1'],
    proxy: {
      '/api': {
        target: 'http://web:8000',
        changeOrigin: true
      }
    }
  }
})
