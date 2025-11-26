import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 3000,
<<<<<<< HEAD
<<<<<<< HEAD
    allowedHosts: ['.ngrok-free.app', 'sportpredict_frontend', 'bore.pub', 'localhost', '127.0.0.1'],
=======
    allowedHosts: ['75c9e95909bd.ngrok-free.app', 'sportpredict_frontend', 'bore.pub', 'localhost', '127.0.0.1'],
>>>>>>> d381094 (v0.14)
=======
    allowedHosts: ['75c9e95909bd.ngrok-free.app', 'sportpredict_frontend', 'bore.pub', 'localhost', '127.0.0.1'],
>>>>>>> d381094 (v0.14)
    proxy: {
      '/api': {
        target: 'http://web:8000',
        changeOrigin: true
      }
    }
  }
})
