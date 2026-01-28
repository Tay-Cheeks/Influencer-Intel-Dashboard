# SaaS Refactoring Plan - Influencer Intel Dashboard

## Overview
Transform the MVP into a production-ready SaaS platform with:
- Professional report generation UI with graphs
- PayPal subscription payment integration
- User authentication and authorization
- Database-backed user data persistence
- Vercel deployment readiness

---

## Architecture Design

### Technology Stack

#### Frontend (Next.js 16)
- **Framework**: Next.js 16 with App Router
- **Styling**: TailwindCSS 4
- **Charts**: Recharts (for data visualization)
- **Auth**: NextAuth.js v5 (Auth.js)
- **Payment**: PayPal JavaScript SDK
- **State**: React Context API (existing AnalysisContext)

#### Backend (FastAPI)
- **Framework**: FastAPI
- **Database**: PostgreSQL (via Supabase or Neon)
- **ORM**: SQLAlchemy
- **Auth**: JWT tokens
- **Deployment**: Render / Railway / Fly.io

#### Database Schema
```sql
-- Users table
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  name VARCHAR(255),
  subscription_tier VARCHAR(50) DEFAULT 'free',
  subscription_status VARCHAR(50) DEFAULT 'inactive',
  paypal_subscription_id VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Analyses table
CREATE TABLE analyses (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  channel_id VARCHAR(255),
  channel_name VARCHAR(255) NOT NULL,
  channel_url TEXT,
  region VARCHAR(100),
  subscribers INTEGER,
  median_views INTEGER,
  average_views INTEGER,
  client_currency VARCHAR(10),
  creator_currency VARCHAR(10),
  quoted_fee_client DECIMAL(10, 2),
  target_margin_pct DECIMAL(5, 2),
  target_cpm DECIMAL(10, 2),
  raw_data JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Subscription plans table
CREATE TABLE subscription_plans (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(100) NOT NULL,
  price_zar DECIMAL(10, 2) NOT NULL,
  price_usd DECIMAL(10, 2) NOT NULL,
  paypal_plan_id VARCHAR(255),
  features JSONB,
  analysis_limit INTEGER,
  created_at TIMESTAMP DEFAULT NOW()
);
```

---

## Implementation Phases

### Phase 1: Report Generation UI ✅

**Goal**: Create a professional report view with graphs and breakdowns

**Components to Build**:

1. **Report Layout Component** (`/frontend/components/report/ReportLayout.tsx`)
   - Full-page report view
   - Print-friendly layout
   - Export to PDF capability

2. **Channel Performance Card** (`/frontend/components/report/ChannelCard.tsx`)
   - Channel info (name, subs, region)
   - Key metrics display
   - Engagement indicators

3. **Charts Components**:
   - `ViewsChart.tsx` - Line/bar chart showing views over time
   - `EngagementChart.tsx` - Engagement rate visualization
   - `ConsistencyChart.tsx` - View consistency/volatility

4. **Video Breakdown Table** (`/frontend/components/report/VideoTable.tsx`)
   - Sortable table of recent videos
   - Views, likes, comments, engagement rate
   - Duration and publish date

5. **Metrics Summary** (`/frontend/components/report/MetricsSummary.tsx`)
   - Mean/median views
   - Engagement rate
   - Risk level indicator
   - CPM calculations

**Dependencies to Install**:
```bash
cd frontend
pnpm add recharts lucide-react
pnpm add -D @types/recharts
```

**New Route**: `/app/analyse/[id]/report` - Full report view

---

### Phase 2: Database Integration

**Goal**: Set up PostgreSQL database and migrate from localStorage to server

**Backend Tasks**:

1. **Database Setup**:
   - Create Supabase/Neon project
   - Run schema migrations
   - Set up connection pooling

2. **SQLAlchemy Models** (`/backend/src/models/`):
   - `user.py` - User model
   - `analysis.py` - Analysis model
   - `subscription.py` - Subscription plan model

3. **Database Service** (`/backend/src/services/database.py`):
   - Connection management
   - CRUD operations
   - Transaction handling

4. **Update API Routes**:
   - Add user_id to analysis endpoints
   - Create user management endpoints
   - Add subscription status checks

**Dependencies**:
```txt
sqlalchemy==2.0.25
psycopg2-binary==2.9.9
alembic==1.13.1
```

---

### Phase 3: User Authentication

**Goal**: Implement secure user authentication with NextAuth.js and JWT

**Frontend Tasks**:

1. **Install NextAuth.js**:
```bash
cd frontend
pnpm add next-auth@beta
pnpm add bcryptjs
pnpm add -D @types/bcryptjs
```

2. **Auth Configuration** (`/frontend/app/api/auth/[...nextauth]/route.ts`):
   - Credentials provider
   - JWT strategy
   - Session callbacks

3. **Auth Components**:
   - `LoginForm.tsx` - Email/password login
   - `SignupForm.tsx` - User registration
   - `AuthGuard.tsx` - Protected route wrapper

4. **Update Routes**:
   - `/login` - Login page
   - `/signup` - Registration page
   - Protect `/app/*` routes with middleware

**Backend Tasks**:

1. **Auth Endpoints** (`/backend/app/api/auth_routes.py`):
   - `POST /api/auth/register` - User registration
   - `POST /api/auth/login` - User login (returns JWT)
   - `GET /api/auth/me` - Get current user
   - `POST /api/auth/refresh` - Refresh token

2. **JWT Utilities** (`/backend/src/utils/jwt.py`):
   - Token generation
   - Token verification
   - Password hashing

**Dependencies**:
```txt
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
```

---

### Phase 4: PayPal Integration

**Goal**: Enable subscription payments via PayPal

**PayPal Setup**:
1. Create PayPal Developer account
2. Create subscription plans in PayPal dashboard
3. Get Client ID and Secret

**Frontend Tasks**:

1. **Install PayPal SDK**:
```bash
cd frontend
pnpm add @paypal/react-paypal-js
```

2. **PayPal Components**:
   - `PayPalProvider.tsx` - Wrap app with PayPal context
   - `SubscriptionButton.tsx` - PayPal subscription button
   - `PaymentSuccess.tsx` - Success page after payment

3. **Update Pricing Page**:
   - Add PayPal buttons to each plan
   - Handle subscription approval
   - Redirect to success page

**Backend Tasks**:

1. **PayPal Service** (`/backend/src/services/paypal.py`):
   - Verify subscription webhook
   - Update user subscription status
   - Handle subscription events (created, cancelled, expired)

2. **Webhook Endpoint** (`/backend/app/api/webhook_routes.py`):
   - `POST /api/webhooks/paypal` - Handle PayPal webhooks

**Environment Variables**:
```env
# Frontend
NEXT_PUBLIC_PAYPAL_CLIENT_ID=your_client_id

# Backend
PAYPAL_CLIENT_ID=your_client_id
PAYPAL_CLIENT_SECRET=your_secret
PAYPAL_MODE=sandbox  # or 'live'
```

---

### Phase 5: Subscription Management

**Goal**: Enforce subscription limits and provide management UI

**Features**:

1. **Usage Tracking**:
   - Count analyses per user per month
   - Check against plan limits
   - Display usage in UI

2. **Subscription Management Page** (`/app/settings/subscription`):
   - Current plan display
   - Usage statistics
   - Upgrade/downgrade options
   - Cancel subscription

3. **Middleware Protection**:
   - Check subscription status before analysis
   - Return 403 if limit reached
   - Prompt upgrade in UI

---

### Phase 6: Deployment Preparation

**Goal**: Configure for production deployment

**Frontend (Vercel)**:

1. **Environment Variables**:
```env
NEXT_PUBLIC_API_BASE_URL=https://your-api.onrender.com
NEXT_PUBLIC_PAYPAL_CLIENT_ID=your_client_id
NEXTAUTH_SECRET=your_secret
NEXTAUTH_URL=https://your-app.vercel.app
DATABASE_URL=postgresql://...
```

2. **Vercel Configuration** (`vercel.json`):
```json
{
  "framework": "nextjs",
  "buildCommand": "cd frontend && pnpm build",
  "installCommand": "cd frontend && pnpm install",
  "outputDirectory": "frontend/.next"
}
```

**Backend (Render/Railway)**:

1. **Dockerfile**:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. **Environment Variables**:
```env
DATABASE_URL=postgresql://...
YOUTUBE_API_KEY=your_key
PAYPAL_CLIENT_ID=your_id
PAYPAL_CLIENT_SECRET=your_secret
JWT_SECRET=your_secret
CORS_ORIGINS=https://your-app.vercel.app
```

3. **Update CORS**:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-app.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Testing Checklist

### Report Generation
- [ ] Report displays channel information correctly
- [ ] Charts render with real data
- [ ] Video table is sortable
- [ ] Metrics calculations are accurate
- [ ] Export to PDF works

### Authentication
- [ ] User can sign up
- [ ] User can log in
- [ ] Protected routes redirect to login
- [ ] Session persists across page reloads
- [ ] Logout works correctly

### PayPal Integration
- [ ] Subscription buttons appear on pricing page
- [ ] PayPal checkout flow works
- [ ] Subscription is activated after payment
- [ ] Webhook updates subscription status
- [ ] User can cancel subscription

### Database
- [ ] Analyses are saved to database
- [ ] User can view saved analyses
- [ ] Analyses are tied to correct user
- [ ] Data persists across sessions

### Deployment
- [ ] Frontend builds successfully
- [ ] Backend starts without errors
- [ ] Environment variables are set
- [ ] CORS allows frontend domain
- [ ] API endpoints are accessible

---

## Timeline Estimate

- **Phase 1** (Report UI): 2-3 hours
- **Phase 2** (Database): 1-2 hours
- **Phase 3** (Auth): 2-3 hours
- **Phase 4** (PayPal): 2-3 hours
- **Phase 5** (Subscription Management): 1-2 hours
- **Phase 6** (Deployment): 1-2 hours

**Total**: 9-15 hours of development work

---

## Next Steps

1. ✅ Create this plan
2. Start with Phase 1: Report Generation UI
3. Install dependencies
4. Build components
5. Test locally
6. Commit and push to GitHub
7. Move to next phase

---

## Notes

- All work will be done on the `feature/saas-refactoring` branch
- Regular commits with descriptive messages
- Test each feature before moving to the next
- Document any API changes in README
- Keep the existing MVP functionality intact
