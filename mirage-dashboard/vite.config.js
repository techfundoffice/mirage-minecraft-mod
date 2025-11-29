import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0', // Listen on all interfaces
    port: 5173,
    strictPort: true,
    cors: true,
    hmr: {
      host: '5173-ims7flew2qqlmi3wl6flu-de59bda9.sandbox.novita.ai',
      protocol: 'wss',
      clientPort: 443
    }
  }
})
