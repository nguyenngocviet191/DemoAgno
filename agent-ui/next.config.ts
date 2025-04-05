import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  /* config options here */
  async rewrites() {
    return [
      {
        source: '/api/playground/:path*',
        destination: 'http://localhost:7777/v1/playground/:path*',
      },
    ]
  },
}

export default nextConfig
