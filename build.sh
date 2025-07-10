#!/bin/bash
# Build script for Vercel deployment

# Install dependencies
npm install

# Build Tailwind CSS
npx tailwindcss -i ./input.css -o ./static/output.css --minify

echo "Build completed successfully!" 