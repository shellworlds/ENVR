/**

ENVR11 Travel Dashboard - Next.js Configuration

Server-side rendering and optimization
*/

/** @type {import('next').NextConfig} /
const nextConfig = {
reactStrictMode: true,
swcMinify: true,
images: {
domains: ['localhost', 'travel-api.envr11.com'],
},
async rewrites() {
return [
{
source: '/api/:path',
destination: 'http://localhost:8000/api/:path',
},
{
source: '/quantum/:path',
destination: 'http://localhost:8081/:path*',
},
];
},
env: {
NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
NEXT_PUBLIC_QUANTUM_URL: process.env.NEXT_PUBLIC_QUANTUM_URL || 'http://localhost:8081',
NEXT_PUBLIC_APP_VERSION: '1.0.0',
},
compiler: {
styledComponents: true,
},
experimental: {
serverActions: true,
},
};

module.exports = nextConfig;
