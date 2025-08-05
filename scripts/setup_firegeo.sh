#!/bin/bash

set -e

echo "🔥 Setting up Firegeo Next.js App"
echo "=================================="

# Check if firegeo directory already exists
if [ -d "firegeo" ]; then
    echo "⚠️  Firegeo directory already exists. Removing..."
    rm -rf firegeo
fi

# Clone the Firegeo repository
echo "📥 Cloning Firegeo repository..."
git clone https://github.com/mendableai/firegeo.git

# Copy Firegeo files to current directory
echo "📋 Copying Firegeo files..."
cp -r firegeo/* .
cp firegeo/.* . 2>/dev/null || true

# Clean up the cloned directory
rm -rf firegeo

# Update package.json to work with our setup and use Bun
echo "🔧 Updating package.json for containerized setup with Bun..."
cat > package.json << 'EOF'
{
  "name": "pyclarity-firegeo",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev --turbopack",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "setup": "node setup.js",
    "setup:autumn": "tsx scripts/setup-autumn.ts",
    "setup:stripe-portal": "tsx scripts/setup-stripe-portal.ts",
    "db:generate": "drizzle-kit generate",
    "db:migrate": "drizzle-kit migrate",
    "db:push": "drizzle-kit push",
    "db:studio": "drizzle-kit studio",
    "db:drop": "drizzle-kit drop"
  },
  "dependencies": {
    "@ai-sdk/anthropic": "^1.2.12",
    "@ai-sdk/google": "^1.2.22",
    "@ai-sdk/openai": "^1.3.23",
    "@ai-sdk/perplexity": "^1.1.9",
    "@mendable/firecrawl-js": "^1.29.1",
    "@radix-ui/react-dialog": "^1.1.14",
    "@radix-ui/react-label": "^2.1.7",
    "@radix-ui/react-progress": "^1.1.7",
    "@radix-ui/react-select": "^2.2.5",
    "@radix-ui/react-slot": "^1.2.3",
    "@radix-ui/react-switch": "^1.2.5",
    "@radix-ui/react-tabs": "^1.1.12",
    "@tanstack/react-query": "^5.82.0",
    "ai": "^4.3.17",
    "autumn-js": "^0.0.96",
    "better-auth": "^1.2.12",
    "class-variance-authority": "^0.7.1",
    "clsx": "^2.1.1",
    "date-fns": "^4.1.0",
    "drizzle-kit": "^0.31.4",
    "drizzle-orm": "^0.44.2",
    "eventsource-parser": "^3.0.3",
    "lucide-react": "^0.525.0",
    "next": "15.3.5",
    "node-fetch": "^2.7.0",
    "pg": "^8.16.3",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "react-markdown": "^10.1.0",
    "recharts": "^3.1.0",
    "remark-gfm": "^4.0.1",
    "tailwindcss": "^4.0.0-alpha.25",
    "tailwind-merge": "^2.5.4",
    "tailwindcss-animate": "^1.0.7",
    "typescript": "^5.4.0",
    "zod": "^3.24.1"
  },
  "devDependencies": {
    "@types/node": "^20",
    "@types/react": "^18",
    "@types/react-dom": "^18",
    "eslint": "^8",
    "eslint-config-next": "15.3.4",
    "tsx": "^4.19.2"
  }
}
EOF

# Create a basic .env.local file
echo "🔐 Creating .env.local template..."
cat > .env.local << 'EOF'
# Database
DATABASE_URL=postgresql://pyclarity:pyclarity@postgres:5432/pyclarity

# Authentication
BETTER_AUTH_SECRET=your-secret-key-here
BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_APP_URL=http://localhost:3000

# Billing
AUTUMN_SECRET_KEY=your-autumn-key-here

# Brand Monitor
FIRECRAWL_API_KEY=your-firecrawl-key-here

# Email
RESEND_API_KEY=your-resend-key-here
EMAIL_FROM=your-email@example.com

# AI Providers (add what you need)
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
PERPLEXITY_API_KEY=
GOOGLE_GENERATIVE_AI_API_KEY=
EOF

# Create next.config.js for standalone output
echo "⚙️  Creating Next.js configuration..."
cat > next.config.js << 'EOF'
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  serverExternalPackages: ['better-auth'],
}

module.exports = nextConfig
EOF

# Create tailwind.config.js for v4
echo "🎨 Creating Tailwind CSS v4 configuration..."
cat > tailwind.config.js << 'EOF'
/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
    './src/**/*.{ts,tsx}',
  ],
  prefix: "",
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}
EOF

# Create tsconfig.json with latest TypeScript
echo "📝 Creating TypeScript configuration..."
cat > tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "lib": ["dom", "dom.iterable", "es6"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "target": "ES2017",
    "plugins": [
      {
        "name": "next"
      }
    ],
    "baseUrl": ".",
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
EOF

# Create global CSS file with Tailwind v4
echo "🎨 Creating global CSS with Tailwind v4..."
mkdir -p app
cat > app/globals.css << 'EOF'
@import "tailwindcss";

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96%;
    --secondary-foreground: 222.2 84% 4.9%;
    --muted: 210 40% 96%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96%;
    --accent-foreground: 222.2 84% 4.9%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 222.2 84% 4.9%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;
    --popover: 222.2 84% 4.9%;
    --popover-foreground: 210 40% 98%;
    --primary: 210 40% 98%;
    --primary-foreground: 222.2 47.4% 11.2%;
    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;
    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;
    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 212.7 26.8% 83.9%;
  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
  }
}
EOF

echo "✅ Firegeo setup complete!"
echo ""
echo "🚀 Next steps:"
echo "1. Run: docker compose up --watch"
echo "2. Visit: http://localhost:3000"
echo ""
echo "📝 Don't forget to update .env.local with your API keys!" 