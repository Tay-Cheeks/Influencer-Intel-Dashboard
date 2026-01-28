# Influencer Intel Dashboard

A comprehensive SaaS platform for analyzing YouTube creator performance and calculating campaign costs. Built for brands and agencies to make data-driven influencer marketing decisions.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Next.js](https://img.shields.io/badge/Next.js-16-black)
![FastAPI](https://img.shields.io/badge/FastAPI-0.128-green)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue)

---

## 🚀 Features

### Analysis & Reporting
- **YouTube Channel Analysis**: Fetch and analyze creator performance metrics
- **Interactive Charts**: Visualize views, engagement, and consistency
- **Video Breakdown**: Detailed table with sortable metrics
- **Risk Assessment**: Automated risk scoring based on volatility
- **CPM Calculations**: Calculate effective CPM and compare to targets

### SaaS Platform
- **User Authentication**: Secure login/signup with NextAuth.js
- **Protected Routes**: App area requires authentication
- **Subscription Management**: PayPal-powered subscription plans
- **User Dashboard**: Save and manage multiple analyses
- **Responsive Design**: Works on desktop, tablet, and mobile

### Brand Tools
- **Campaign Costing**: Calculate talent fees and margins
- **Currency Conversion**: Multi-currency support with live FX rates
- **Pricing Calculator**: Mode 1 (standalone) and Mode 2 (analysis-based)
- **Export Reports**: PDF export capability (coming soon)

---

## 🛠️ Tech Stack

### Frontend
- **Framework**: Next.js 16 (App Router)
- **Language**: TypeScript
- **Styling**: TailwindCSS 4
- **Charts**: Recharts
- **Auth**: NextAuth.js v5
- **Payment**: PayPal JavaScript SDK
- **Icons**: Lucide React

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.11
- **API Client**: Google API Client (YouTube Data API v3)
- **Data Processing**: Custom analysis engine
- **FX Rates**: Frankfurter API

### Deployment
- **Frontend**: Vercel
- **Backend**: Render / Railway / Fly.io
- **Database**: PostgreSQL (Supabase / Neon)

---

## 📦 Project Structure

```
Influencer-Intel-Dashboard/
├── frontend/                  # Next.js frontend application
│   ├── app/
│   │   ├── (public)/         # Public pages (landing, pricing, tutorial)
│   │   ├── (auth)/           # Auth pages (login, signup)
│   │   ├── (app)/            # Protected app pages (analyse, saved, calculator)
│   │   ├── api/              # API routes (auth, webhooks)
│   │   └── layout.tsx        # Root layout
│   ├── components/           # React components
│   │   ├── report/           # Report components (charts, tables, cards)
│   │   ├── Sidebar.tsx       # App sidebar navigation
│   │   └── ThemeProvider.tsx # Dark/light theme
│   ├── context/              # React context providers
│   │   └── AnalysisContext.tsx
│   └── middleware.ts         # Route protection middleware
│
├── backend/                   # FastAPI backend application
│   ├── app/
│   │   ├── api/              # API routes
│   │   │   └── routes.py     # Main API endpoints
│   │   └── main.py           # FastAPI app entry point
│   ├── src/
│   │   ├── youtube/          # YouTube API client
│   │   ├── analysis/         # Analysis engine
│   │   ├── services/         # Business logic services
│   │   └── utils/            # Utility functions
│   └── requirements.txt      # Python dependencies
│
├── DEPLOYMENT_GUIDE.md       # Comprehensive deployment guide
├── REFACTORING_PLAN.md       # Technical implementation plan
└── README.md                 # This file
```

---

## 🚦 Getting Started

### Prerequisites

- Node.js 22+ and pnpm
- Python 3.11+
- YouTube Data API v3 key
- PayPal Developer account (for payments)

### 1. Clone the Repository

```bash
git clone https://github.com/Thando-init/Influencer-Intel-Dashboard.git
cd Influencer-Intel-Dashboard
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export YOUTUBE_API_KEY=your_youtube_api_key

# Run the backend
uvicorn app.main:app --reload --port 8000
```

Backend will be available at `http://localhost:8000`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
pnpm install

# Copy environment variables
cp .env.example .env.local

# Edit .env.local and add your values:
# - NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
# - NEXTAUTH_SECRET=your-secret-key
# - NEXT_PUBLIC_PAYPAL_CLIENT_ID=your-paypal-client-id

# Run the frontend
pnpm dev
```

Frontend will be available at `http://localhost:3000`

### 4. Access the Application

1. Open `http://localhost:3000` in your browser
2. Create an account at `/signup`
3. Login and start analyzing YouTube creators!

---

## 📖 Usage Guide

### Running an Analysis

1. **Navigate to Analyse Page**: `/app/analyse`
2. **Enter YouTube URL**: Paste channel URL or video URL
3. **Set Video Count**: Choose how many recent videos to analyze (1-25)
4. **Add Brand Inputs** (optional):
   - Creator region
   - Client/Creator currencies
   - Quoted fee
   - Agency margin %
   - Target CPM
5. **Run Analysis**: Click "Run analysis" button
6. **View Report**: See comprehensive report with charts and metrics

### Using the Calculator

1. **Navigate to Calculator**: `/app/calculator`
2. **Mode 1 (Standalone)**: Enter all values manually
3. **Mode 2 (Analysis-based)**: Use data from saved analysis
4. **Calculate**: Get talent payout, CPM, and margin breakdown

### Managing Saved Analyses

1. **Navigate to Saved**: `/app/saved`
2. **View List**: See all your saved analyses
3. **Click to Activate**: Select an analysis to use in calculator
4. **Recent Analyses**: Quick access from sidebar

---

## 🎨 Features Walkthrough

### Report Components

#### Channel Card
- Channel name and subscriber count
- Region and key metrics
- Risk level indicator
- Link to YouTube channel

#### Views Chart
- Bar or line chart toggle
- Shows views for recent videos
- Median and average benchmarks
- Interactive tooltips

#### Engagement Chart
- Engagement rate per video
- Color-coded by performance
- Hover for detailed metrics

#### Video Table
- Sortable by any column
- Views, likes, comments, engagement
- Video title and publish date
- Duration display

#### Metrics Summary
- Median and average views
- Engagement, like, and comment rates
- Volatility ratio
- CPM analysis with target comparison

---

## 🔐 Authentication Flow

### Sign Up
1. User enters name, email, and password
2. Password is hashed with bcrypt
3. User record created in database
4. Redirect to login page

### Login
1. User enters email and password
2. Credentials verified against database
3. JWT token generated
4. Session created with NextAuth.js
5. Redirect to app dashboard

### Protected Routes
- All `/app/*` routes require authentication
- Middleware checks for valid session
- Unauthenticated users redirected to login
- Callback URL preserved for post-login redirect

---

## 💳 Payment Integration

### Subscription Plans

**Starter Plan** - R499/month ($29)
- 30 analyses per month
- Key metrics and charts
- Campaign costing calculator
- Email support

**Pro Plan** - R999/month ($59) ⭐ Recommended
- Unlimited analyses
- Saved creators with notes
- PDF/CSV exports (coming soon)
- Priority support

**Team Plan** - Custom pricing
- Multi-seat access
- Shared saved lists
- Usage controls
- SLA and onboarding

### PayPal Integration

1. User selects plan on pricing page
2. PayPal checkout modal opens
3. User completes payment
4. Webhook updates subscription status
5. User gains access to plan features

---

## 🌐 API Endpoints

### Backend API

#### Health Check
```
GET /api/health
```
Returns API status

#### YouTube Analysis
```
POST /api/analysis
Body: {
  "youtube_url": "https://youtube.com/...",
  "video_count": 8
}
```
Returns channel data, videos, and metrics

#### FX Rates
```
GET /api/fx?base=USD&symbols=ZAR,EUR,GBP
```
Returns current exchange rates

---

## 🧪 Testing

### Frontend Testing

```bash
cd frontend
pnpm test
```

### Backend Testing

```bash
cd backend
pytest
```

### Manual Testing Checklist

- [ ] User can sign up
- [ ] User can login
- [ ] Protected routes work
- [ ] Analysis runs successfully
- [ ] Report displays correctly
- [ ] Charts render properly
- [ ] Table is sortable
- [ ] Sidebar shows user info
- [ ] Logout works
- [ ] Theme toggle works

---

## 🚀 Deployment

See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) for comprehensive deployment instructions.

### Quick Deploy

**Frontend (Vercel)**
```bash
vercel --prod
```

**Backend (Render)**
- Connect GitHub repository
- Set environment variables
- Deploy from dashboard

---

## 🔧 Configuration

### Environment Variables

#### Frontend
```env
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
NEXTAUTH_SECRET=your-secret-key
NEXTAUTH_URL=http://localhost:3000
NEXT_PUBLIC_PAYPAL_CLIENT_ID=your-paypal-client-id
```

#### Backend
```env
YOUTUBE_API_KEY=your-youtube-api-key
DATABASE_URL=postgresql://...
PAYPAL_CLIENT_ID=your-paypal-client-id
PAYPAL_CLIENT_SECRET=your-paypal-secret
CORS_ORIGINS=http://localhost:3000
```

---

## 📝 Development Notes

### Current Implementation

- ✅ Report generation with charts
- ✅ User authentication
- ✅ PayPal payment integration
- ✅ Protected routes
- ✅ Responsive design
- ✅ Dark/light theme
- ⚠️ In-memory user storage (MVP)

### Planned Features

- [ ] PostgreSQL database integration
- [ ] PDF export for reports
- [ ] CSV export for data
- [ ] Email notifications
- [ ] Usage limit enforcement
- [ ] Team collaboration features
- [ ] Advanced filtering and search
- [ ] Comparison mode (multiple creators)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **Thando** - Initial work - [@Thando-init](https://github.com/Thando-init)

---

## 🙏 Acknowledgments

- YouTube Data API v3
- Next.js team for the amazing framework
- FastAPI for the blazing-fast backend
- Recharts for beautiful visualizations
- PayPal for payment processing
- Vercel for hosting

---

## 📞 Support

For support, email support@influencerintel.com or open an issue on GitHub.

---

## 🔗 Links

- [Live Demo](https://your-app.vercel.app)
- [Documentation](./DEPLOYMENT_GUIDE.md)
- [GitHub Repository](https://github.com/Thando-init/Influencer-Intel-Dashboard)
- [Report Issues](https://github.com/Thando-init/Influencer-Intel-Dashboard/issues)

---

**Made with ❤️ for brands and agencies making data-driven influencer marketing decisions.**
