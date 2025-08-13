# Zimmer Admin Dashboard

A professional admin dashboard for Zimmer's internal management and automation tracking system.

## Features

- **Dashboard Overview**: Key metrics and statistics
- **Client Management**: View and manage registered clients
- **Knowledge Base**: Manage AI responses and knowledge entries
- **Token Usage**: Monitor AI token consumption
- **Payments**: Track revenue and payment history
- **Fallback Logs**: Monitor unanswered questions

## Tech Stack

- **Next.js 14** with TypeScript
- **TailwindCSS** for styling
- **Axios** for API communication
- **React 18** with modern hooks

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Create environment file:
```bash
cp .env.example .env.local
```

3. Update `.env.local` with your API URL:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

4. Run the development server:
```bash
npm run dev
```

5. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
zimmer-admin-dashboard/
├── components/          # Reusable UI components
│   ├── Layout.tsx      # Main layout wrapper
│   ├── Sidebar.tsx     # Navigation sidebar
│   └── Topbar.tsx      # Top navigation bar
├── pages/              # Next.js pages
│   ├── index.tsx       # Dashboard home
│   ├── clients.tsx     # Client management
│   ├── knowledge.tsx   # Knowledge base
│   ├── usage.tsx       # Token usage
│   ├── payments.tsx    # Payment tracking
│   └── fallbacks.tsx   # Fallback logs
├── lib/                # Utility libraries
│   └── api.ts          # Axios API client
├── styles/             # Global styles
│   └── globals.css     # TailwindCSS imports
└── public/             # Static assets
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## API Integration

The dashboard connects to the Zimmer backend API at `http://localhost:8000`. Make sure your backend server is running before using the dashboard.

## Customization

- **Colors**: Modify `tailwind.config.js` to add custom colors
- **Layout**: Edit `components/Layout.tsx` for layout changes
- **Navigation**: Update `components/Sidebar.tsx` for menu changes
- **Styling**: Use TailwindCSS classes throughout the application

## Deployment

1. Build the application:
```bash
npm run build
```

2. Start the production server:
```bash
npm run start
```

Or deploy to Vercel, Netlify, or your preferred hosting platform. 