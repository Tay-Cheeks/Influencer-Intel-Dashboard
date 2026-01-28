# Deployment Guide - Influencer Intel Dashboard

This guide will help you deploy your YouTube creator analysis SaaS platform to production.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Frontend Deployment (Vercel)](#frontend-deployment-vercel)
3. [Backend Deployment (Render/Railway)](#backend-deployment-renderrailway)
4. [Database Setup](#database-setup)
5. [PayPal Configuration](#paypal-configuration)
6. [Environment Variables](#environment-variables)
7. [Testing the Deployment](#testing-the-deployment)
8. [Post-Deployment Checklist](#post-deployment-checklist)

---

## Prerequisites

Before deploying, ensure you have:

- ✅ GitHub account with this repository
- ✅ Vercel account (free tier works)
- ✅ Render/Railway account (for backend)
- ✅ PayPal Business account
- ✅ PostgreSQL database (Supabase/Neon recommended)
- ✅ YouTube Data API key

---

## Frontend Deployment (Vercel)

### Step 1: Connect Repository to Vercel

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click "Add New Project"
3. Import your GitHub repository: `Thando-init/Influencer-Intel-Dashboard`
4. Configure project settings:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `pnpm build`
   - **Output Directory**: `.next`
   - **Install Command**: `pnpm install`

### Step 2: Configure Environment Variables

In Vercel project settings, add these environment variables:

```env
# API Configuration
NEXT_PUBLIC_API_BASE_URL=https://your-backend.onrender.com

# NextAuth Configuration
NEXTAUTH_SECRET=<generate-a-random-secret-key>
NEXTAUTH_URL=https://your-app.vercel.app

# PayPal Configuration
NEXT_PUBLIC_PAYPAL_CLIENT_ID=<your-paypal-client-id>
```

**Generate NEXTAUTH_SECRET:**
```bash
openssl rand -base64 32
```

### Step 3: Deploy

1. Click "Deploy"
2. Wait for build to complete
3. Your app will be live at `https://your-app.vercel.app`

### Step 4: Configure Custom Domain (Optional)

1. Go to Project Settings → Domains
2. Add your custom domain
3. Update DNS records as instructed
4. Update `NEXTAUTH_URL` to your custom domain

---

## Backend Deployment (Render/Railway)

### Option A: Deploy to Render

#### Step 1: Create Render Account

1. Go to [render.com](https://render.com) and sign up
2. Connect your GitHub account

#### Step 2: Create Web Service

1. Click "New +" → "Web Service"
2. Connect your repository
3. Configure service:
   - **Name**: `influencer-intel-api`
   - **Region**: Choose closest to your users
   - **Branch**: `feature/saas-refactoring` (or `main` after merging)
   - **Root Directory**: `backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

#### Step 3: Add Environment Variables

In Render service settings, add:

```env
# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# YouTube API
YOUTUBE_API_KEY=your-youtube-api-key

# PayPal
PAYPAL_CLIENT_ID=your-paypal-client-id
PAYPAL_CLIENT_SECRET=your-paypal-secret
PAYPAL_MODE=live

# JWT
JWT_SECRET=your-jwt-secret

# CORS
CORS_ORIGINS=https://your-app.vercel.app,http://localhost:3000
```

#### Step 4: Deploy

1. Click "Create Web Service"
2. Wait for deployment to complete
3. Your API will be live at `https://your-backend.onrender.com`

### Option B: Deploy to Railway

1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Configure:
   - **Root Directory**: `backend`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables (same as Render)
6. Deploy

---

## Database Setup

### Option A: Supabase (Recommended)

1. Go to [supabase.com](https://supabase.com) and create account
2. Create new project
3. Go to Settings → Database
4. Copy connection string
5. Run migrations (see below)

### Option B: Neon

1. Go to [neon.tech](https://neon.tech)
2. Create new project
3. Copy connection string
4. Run migrations

### Database Schema

Create these tables in your database:

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

-- Indexes
CREATE INDEX idx_analyses_user_id ON analyses(user_id);
CREATE INDEX idx_analyses_created_at ON analyses(created_at DESC);
CREATE INDEX idx_users_email ON users(email);
```

---

## PayPal Configuration

### Step 1: Create PayPal Business Account

1. Go to [paypal.com/business](https://www.paypal.com/business)
2. Sign up for Business account
3. Complete verification

### Step 2: Create Subscription Plans

1. Go to PayPal Developer Dashboard
2. Navigate to Products & Pricing
3. Create subscription plans:

**Starter Plan:**
- Name: Influencer Intel Starter
- Price: $29/month (or R499)
- Billing cycle: Monthly
- Copy the Plan ID

**Pro Plan:**
- Name: Influencer Intel Pro
- Price: $59/month (or R999)
- Billing cycle: Monthly
- Copy the Plan ID

### Step 3: Get API Credentials

1. Go to PayPal Developer Dashboard
2. Navigate to Apps & Credentials
3. Create new app
4. Copy Client ID and Secret
5. Switch to "Live" mode when ready for production

### Step 4: Update Frontend Code

In `frontend/app/(public)/pricing/page.tsx`, update the plan IDs:

```typescript
const plans = [
  {
    id: "starter",
    // ...
    paypalPlanId: "P-XXXXXXXXXXXX", // Your actual Starter plan ID
  },
  {
    id: "pro",
    // ...
    paypalPlanId: "P-XXXXXXXXXXXX", // Your actual Pro plan ID
  },
];
```

### Step 5: Configure Webhooks

1. In PayPal Dashboard, go to Webhooks
2. Add webhook URL: `https://your-backend.onrender.com/api/webhooks/paypal`
3. Subscribe to events:
   - `BILLING.SUBSCRIPTION.CREATED`
   - `BILLING.SUBSCRIPTION.ACTIVATED`
   - `BILLING.SUBSCRIPTION.CANCELLED`
   - `BILLING.SUBSCRIPTION.EXPIRED`

---

## Environment Variables

### Frontend (.env.local for development, Vercel for production)

```env
# API Configuration
NEXT_PUBLIC_API_BASE_URL=https://your-backend.onrender.com

# NextAuth Configuration
NEXTAUTH_SECRET=your-secret-key-min-32-chars
NEXTAUTH_URL=https://your-app.vercel.app

# PayPal Configuration
NEXT_PUBLIC_PAYPAL_CLIENT_ID=your-paypal-client-id
```

### Backend (Render/Railway environment variables)

```env
# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# YouTube API
YOUTUBE_API_KEY=your-youtube-api-key

# PayPal
PAYPAL_CLIENT_ID=your-paypal-client-id
PAYPAL_CLIENT_SECRET=your-paypal-secret
PAYPAL_MODE=live

# JWT
JWT_SECRET=your-jwt-secret-min-32-chars

# CORS
CORS_ORIGINS=https://your-app.vercel.app
```

---

## Testing the Deployment

### 1. Test Frontend

- [ ] Visit your Vercel URL
- [ ] Landing page loads correctly
- [ ] Pricing page displays plans
- [ ] Tutorial page works
- [ ] Dark/Light theme toggle works

### 2. Test Authentication

- [ ] Go to `/signup`
- [ ] Create a new account
- [ ] Verify redirect to login
- [ ] Login with credentials
- [ ] Verify redirect to `/app/analyse`
- [ ] Check sidebar shows user info
- [ ] Test logout

### 3. Test Analysis Flow

- [ ] Paste a YouTube URL
- [ ] Run analysis
- [ ] Verify report displays with:
  - [ ] Channel card
  - [ ] Metrics summary
  - [ ] Views chart
  - [ ] Engagement chart
  - [ ] Video table
- [ ] Check analysis saves to sidebar

### 4. Test PayPal Integration

- [ ] Go to pricing page
- [ ] Click "Start Pro" (or Starter)
- [ ] Verify PayPal checkout opens
- [ ] Complete test payment (use PayPal sandbox)
- [ ] Verify subscription activates

### 5. Test Protected Routes

- [ ] Logout
- [ ] Try to access `/app/analyse`
- [ ] Verify redirect to `/login`
- [ ] Login and verify redirect back to app

---

## Post-Deployment Checklist

### Security

- [ ] Change all default secrets
- [ ] Enable HTTPS only
- [ ] Configure CORS properly
- [ ] Set up rate limiting (optional)
- [ ] Enable PayPal webhook signature verification

### Performance

- [ ] Enable Vercel Analytics
- [ ] Set up error tracking (Sentry recommended)
- [ ] Configure CDN for static assets
- [ ] Optimize images

### Monitoring

- [ ] Set up uptime monitoring (UptimeRobot)
- [ ] Configure backend logging
- [ ] Set up database backups
- [ ] Monitor API usage

### Legal

- [ ] Add Terms of Service page
- [ ] Add Privacy Policy page
- [ ] Add Cookie Policy
- [ ] Configure GDPR compliance (if EU users)

### Marketing

- [ ] Set up Google Analytics
- [ ] Configure SEO meta tags
- [ ] Add social media preview images
- [ ] Set up email notifications (optional)

---

## Troubleshooting

### Frontend Build Fails

**Error:** `Module not found`
- Solution: Check all imports are correct
- Run `pnpm install` locally first
- Verify `package.json` is complete

**Error:** `Environment variable not found`
- Solution: Add all required env vars in Vercel
- Prefix public vars with `NEXT_PUBLIC_`

### Backend Fails to Start

**Error:** `Port already in use`
- Solution: Use `$PORT` environment variable
- Update start command: `--port $PORT`

**Error:** `Database connection failed`
- Solution: Check `DATABASE_URL` format
- Verify database is accessible from Render/Railway
- Check firewall rules

### Authentication Not Working

**Error:** `NextAuth session undefined`
- Solution: Verify `NEXTAUTH_SECRET` is set
- Check `NEXTAUTH_URL` matches your domain
- Clear cookies and try again

### PayPal Integration Issues

**Error:** `PayPal button not showing`
- Solution: Check `NEXT_PUBLIC_PAYPAL_CLIENT_ID` is set
- Verify PayPal SDK is loaded
- Check browser console for errors

**Error:** `Subscription not activating`
- Solution: Verify webhook URL is correct
- Check webhook events are subscribed
- Test webhook with PayPal simulator

---

## Support

If you encounter issues:

1. Check the [GitHub Issues](https://github.com/Thando-init/Influencer-Intel-Dashboard/issues)
2. Review Vercel/Render logs
3. Test locally first with `pnpm dev`
4. Verify all environment variables are set

---

## Next Steps

After successful deployment:

1. **Replace In-Memory Storage**: Migrate from in-memory user store to PostgreSQL
2. **Add Database Persistence**: Connect backend to database for analyses
3. **Enable Real PayPal**: Switch from sandbox to live mode
4. **Add Email Notifications**: Set up transactional emails
5. **Implement Usage Limits**: Enforce subscription plan limits
6. **Add Export Features**: PDF/CSV export for reports
7. **Set Up Analytics**: Track user behavior and conversions

---

## Production Readiness Checklist

- [ ] Database is set up and migrations run
- [ ] All environment variables configured
- [ ] PayPal plans created and IDs added
- [ ] CORS configured for production domain
- [ ] HTTPS enabled on all endpoints
- [ ] Error tracking configured
- [ ] Backup strategy in place
- [ ] Terms of Service and Privacy Policy added
- [ ] Testing completed successfully
- [ ] Monitoring and alerts set up

---

**Congratulations!** 🎉 Your SaaS platform is now live and ready for users.
