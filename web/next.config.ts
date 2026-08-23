import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'export',
  basePath: '/real-estate-leads',
  images: {
    unoptimized: true,
  },
};

export default nextConfig;
