/**

ENVR11 Travel Dashboard - Vite Configuration

Modern build tool for fast development
*/

import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
plugins: [react()],
server: {
port: 3000,
host: true,
proxy: {
'/api': {
target: 'http://localhost:8000',
changeOrigin: true,
secure: false
},
'/quantum': {
target: 'http://localhost:8081',
changeOrigin: true,
secure: false
}
}
},
resolve: {
alias: {
'@': path.resolve(__dirname, './src'),
'@components': path.resolve(__dirname, './components'),
'@utils': path.resolve(__dirname, './utils')
}
},
build: {
outDir: 'dist',
sourcemap: true,
rollupOptions: {
output: {
manualChunks: {
vendor: ['react', 'react-dom', 'axios'],
charts: ['recharts', 'd3'],
ui: ['react-query', 'lodash']
}
}
}
},
css: {
preprocessorOptions: {
scss: {
additionalData: @import "./src/styles/variables.scss";
}
}
}
});
