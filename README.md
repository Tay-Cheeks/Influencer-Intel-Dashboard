## Influencer Intelligence Dashboard

A data-driven analytics dashboard for evaluating YouTube creators using performance metrics, engagement quality, audience loyalty, monetisation indicators, and benchmark-based analysis.

This project is designed to support influencer campaign planning, creator vetting, and performance reporting for agencies, brands, and talent managers.

## Features

- YouTube creator performance analysis
- Mean vs median view distribution diagnostics
- Engagement and audience loyalty metrics
- Risk and anti-fraud signal detection
- Benchmark tier comparison based on subscriber count
- Monetisation metrics (CPM, CPE, CPV, talent cost)
- AI-assisted performance summaries (optional)
- Interactive Streamlit dashboard with charts
- Streamlit Cloud deployment ready

## Architecture Overview
.
├── app.py                      Streamlit application entry point
├── requirements.txt            Python dependencies
├── README.md
├── src/
│   ├── metrics/
│   │   ├── metrics.py          Core metric calculations
│   │   └── example.py          Local testing harness
│   ├── analysis/
│   │   ├── benchmarks.py       Industry benchmark tiers
│   │   └── analyser.py         Comparative analysis logic
│   └── ai/
│       └── openai_utils.py     AI scoring utilities

## Key Metrics Calculated

- Performance
- Mean views
- Median views
- View volatility and risk classification
- Short-form vs long-form content mix
- View velocity (last 7 days)
- Engagement Quality
- Engagement rate
- Like rate
- Comment rate
- Engagement consistency
- Loyalty (views-to-subscriber ratio)

- Monetisation
    CPM (Cost per 1,000 views)
    CPE (Cost per engagement)
    CPV (Cost per view)
    Talent cost after agency margin
    Engagement-adjusted CPM
    Benchmarking System

- Creators are evaluated against tier-specific benchmarks based on subscriber count:

    1. Nano
    2. Micro
    3. Mid-tier
    4. Macro
    5. Mega

Each tier defines expected engagement and loyalty ranges, enabling comparative analysis such as:

- Above benchmark
- Within benchmark
- Below benchmark

## AI Analysis (Optional)

The system can optionally generate:

1. A 0–100 performance score
2. A short qualitative summary of strengths and risks

If no OpenAI API quota is available, the dashboard falls back to a deterministic scoring model.

## Local Development
Requirements

    - Python 3.9+
    - pip

## Setup
git clone git@gitlab.com:Tay-Cheeks/influencer-intel-hub.git
cd influencer-intel-hub
pip install -r requirements.txt

Environment Variables

Create a .env file locally or set system environment variables:

- OPENAI_API_KEY=your_openai_key
- YOUTUBE_API_KEY=your_youtube_key

Running Locally
streamlit run app.py


The app will be available at:

http://localhost:8501

## Streamlit Cloud Deployment

This repository is compatible with Streamlit Cloud.

Deployment requirements:

- app.py at repository root
- requirements.txt present

Secrets configured in Streamlit Cloud settings

Secrets format:

    OPENAI_API_KEY="your_openai_key"
    YOUTUBE_API_KEY="your_youtube_key"

Intended Use

This tool is intended for:

1. Influencer marketing agencies
2. Campaign managers
3. Brand partnerships teams
4. Creator performance audits
5. Pre-campaign vetting and post-campaign reviews

It is not intended to scrape private creator data or bypass platform permissions.

## Roadmap

- Automated YouTube API ingestion via channel URL
- Daily metric refresh with caching
- Campaign-level reporting
- Cross-platform support (TikTok, Instagram)
- Exportable PDF and CSV reports

## Disclaimer

All metrics are estimates derived from publicly available data and provided inputs. They should be used as decision-support tools, not guarantees of campaign outcomes.