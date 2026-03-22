# 🔍 AI Website Auditor

A production-ready tool that combines **web scraping** with **AI analysis** to deliver comprehensive website audits.

Built with **Streamlit**, **Playwright**, and **Google Gemini**.

---

## ✨ Features

- **🎯 Factual Metrics**: Word count, headings, CTAs, links, images, alt text, SEO metadata
- **🤖 AI Insights**: SEO analysis, messaging, CTA effectiveness, UX concerns
- **📊 Structured Output**: Pydantic-validated data with grounded recommendations
- **🔍 Full Transparency**: Complete prompt logging and reasoning trace
- **🐳 Docker Ready**: Production deployment configurations included

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
playwright install chromium
```

### 2. Configure API Key

```bash
# Create .env file
echo "GOOGLE_API_KEY=your_actual_api_key_here" > .env
```

Get your Google API key from: https://makersuite.google.com/app/apikey

### 3. Run the App

```bash
streamlit run app.py
```

Access at http://localhost:8501

---

## 🐳 Docker Deployment

### Local Testing

```bash
# Using Docker Compose (recommended)
docker-compose up -d

# Or using Docker directly
docker build -t website-auditor .
docker run -p 8501:8501 -e GOOGLE_API_KEY=your_key website-auditor
```

### Streamlit Cloud Deployment (Recommended)

**Deploy in 5 minutes for FREE**:

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push
   ```

2. **Pin Python Runtime**:
   - Add `runtime.txt` in repo root with: `python-3.11.9`

3. **Deploy to Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Connect your GitHub repository
   - Select `main` branch and `app.py` as the main file
   - Click "Advanced settings" → "Secrets"
   - Add: `GOOGLE_API_KEY = "your_actual_api_key_here"`
   - Click "Deploy!"

3. **Done!** Your app will be live at `https://your-app-name.streamlit.app`

**Alternative Docker Deployment**:
For production deployments with Docker, see included configurations for Railway, Render, Fly.io, and Google Cloud Run in the repository.

---

## 📁 Project Structure

```
.
├── app.py              # Streamlit UI
├── scraper.py          # Playwright + BeautifulSoup scraping
├── analyzer.py         # Google Gemini AI analysis
├── models.py           # Pydantic data models
├── logger.py           # Prompt logging utility
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker image configuration
├── docker-compose.yml  # Docker Compose setup
├── railway.json        # Railway deployment config
├── render.yaml         # Render deployment config
├── fly.toml            # Fly.io deployment config
└── DEPLOY.md           # Deployment guide
```

---

## 🎯 How It Works

```
User enters URL
    ↓
Playwright scrapes page (handles JavaScript)
    ↓
BeautifulSoup extracts metrics (words, headings, CTAs, links, images)
    ↓
Pydantic validates data → PageMetrics
    ↓
Google Gemini analyzes metrics (grounded in factual data)
    ↓
Pydantic validates AI output → AuditReport
    ↓
Streamlit displays results + prompt logs
```

---

## 📊 Example Output

### Input
```
URL: https://example.com
```

### Factual Metrics (Left Column)
- 1,250 words
- 1 H1, 5 H2s, 8 H3s
- 3 CTAs
- 15 internal links, 5 external links
- 10 images (20% missing alt text)

### AI Insights (Right Column)
> "With only 3 CTAs across 1,250 words (1 per 417 words), conversion opportunities are limited compared to the industry standard of 1 CTA per 200-250 words..."

> "Critical: 20% of images (2/10) lack alt text, creating accessibility barriers and missing SEO opportunities..."

### Recommendations
1. Add alt text to 2 images immediately
2. Increase CTAs from 3 to 6-8 (target 1 per 200 words)
3. Shorten meta description by 10 characters

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Frontend** | Streamlit |
| **Scraping** | Playwright + BeautifulSoup4 |
| **AI** | Google Gemini 2.5 Flash |
| **Validation** | Pydantic v2 |
| **Deployment** | Docker |
| **Language** | Python 3.11+ |

---

## ⚙️ Customization

### Change AI Model
```python
# analyzer.py, line 40
analyst = AuditAnalyst(model_name="gemini-2.5-flash")  # or gemini-2.5-pro
```

### Adjust Temperature
```python
# analyzer.py, line 62
"temperature": 0.3,  # Lower = more consistent (0.0 - 2.0)
```

### Add CTA Keywords
```python
# scraper.py, line 75
cta_keywords = ['sign up', 'buy now', 'your custom keyword']
```

---

## 📈 Metrics Collected

| Category | Metrics |
|----------|---------|
| **Content** | Word count, H1/H2/H3 counts |
| **Conversion** | CTA count (buttons + action links) |
| **Links** | Internal vs. external links |
| **Media** | Image count, % missing alt text |
| **SEO** | Meta title, meta description |

---

## 🔒 Security

- ✅ API keys stored in `.env` (never committed)
- ✅ Environment variables for production
- ✅ `.gitignore` configured properly
- ✅ Docker secrets support
- ✅ HTTPS enabled on all deployment platforms

---

## 💰 Cost Estimation

**Google Gemini 2.5 Flash**:
- ~500-1000 tokens per audit
- **Cost per audit**: < $0.001
- **100 audits**: ~$0.10
- **Free tier**: 15 requests/minute

**Hosting** (see DEPLOY.md for details):
- FREE: Streamlit Cloud, Render (with limitations)
- $5/mo: Railway, DigitalOcean, Fly.io
- Pay-per-use: Google Cloud Run (~$5-20/mo)

---

## 🚀 Deployment Checklist

- [ ] Google API key obtained from [Google AI Studio](https://makersuite.google.com/app/apikey)
- [ ] `.env` file created locally for testing
- [ ] Tested locally with `streamlit run app.py`
- [ ] Code pushed to GitHub repository
- [ ] Connected GitHub to [Streamlit Cloud](https://share.streamlit.io)
- [ ] Added `GOOGLE_API_KEY` to Streamlit secrets
- [ ] Deployed and verified live URL works

---

## 📚 Project Files

Core application files and deployment configurations are included in this repository:
- **Core**: `app.py`, `scraper.py`, `analyzer.py`, `models.py`, `logger.py`
- **Docker**: `Dockerfile`, `docker-compose.yml`, `.dockerignore`
- **Cloud Configs**: `railway.json`, `render.yaml`, `fly.toml` (for alternative deployments)

---

## 🔄 Trade-offs & Design Decisions

### 1. Playwright vs. Requests for Scraping

**Decision**: Used Playwright instead of simpler libraries like `requests` or `httpx`.

**Trade-off**:
- ✅ **Benefit**: Handles JavaScript-rendered content, SPAs, and dynamic loading. Many modern websites (React, Vue, Angular) require JavaScript execution to display content.
- ❌ **Cost**: Larger Docker image (~500MB vs ~100MB) and slower cold starts (~3-5s vs <1s). Requires bundled Chromium browser.

**Why it's worth it**: Modern websites increasingly rely on client-side rendering. A simpler approach would fail on 40-60% of target websites, making the tool unreliable for production use. The image size trade-off is acceptable for deployment platforms with container caching (Railway, Cloud Run, Fly.io).

---

### 2. Gemini 1.5 Flash vs. Gemini 1.5 Pro

**Decision**: Used Gemini 1.5 Flash as the default model instead of Pro.

**Trade-off**:
- ✅ **Benefit**: 10x faster inference (~1-2s vs ~5-10s) and 20x cheaper ($0.075 vs $1.50 per 1M input tokens). Enables real-time analysis without API cost concerns.
- ❌ **Cost**: Slightly less nuanced insights on complex edge cases. Pro excels at deeper reasoning and comparative analysis.

**Why it's worth it**: For website audits, Flash provides sufficient accuracy while maintaining sub-5-second response times. The grounded prompt engineering (forcing metric citations) compensates for any reasoning gaps. Users can easily switch to Pro by changing one line in `analyzer.py` if needed.

---

### 3. Separate Scraping Layer vs. Direct HTML to LLM

**Decision**: Extracted structured metrics (PageMetrics) before sending to AI, rather than feeding raw HTML.

**Trade-off**:
- ✅ **Benefit**:
  - **Token efficiency**: Sends ~200 tokens (structured metrics) instead of ~5,000-50,000 tokens (raw HTML)
  - **Grounding**: Forces AI to reference factual data, reducing hallucinations
  - **Cost savings**: 25-250x fewer tokens per request (~$0.0001 vs ~$0.005-0.05 per audit)
- ❌ **Cost**: Cannot analyze visual layout, styling, or UX patterns that require HTML/CSS context.

**Why it's worth it**: The cost and accuracy benefits far outweigh the loss of layout analysis. For visual insights, a future multimodal approach (screenshots) would be more effective than raw HTML anyway.

---

### 4. Pydantic Validation vs. Schema-less JSON

**Decision**: Used Pydantic models for both input (PageMetrics) and output (AuditReport).

**Trade-off**:
- ✅ **Benefit**: Type safety, automatic validation, clear data contracts, easier debugging, and self-documenting code.
- ❌ **Cost**: Slightly more rigid structure. Adding new metrics requires schema updates.

**Why it's worth it**: Type safety catches bugs at development time rather than production. The clarity of defined schemas makes the codebase maintainable and extensible.

---

## 🚀 Future Improvements

With additional time, here are high-impact enhancements that would significantly extend the tool's capabilities:

### 1. Multimodal Visual Analysis

**Objective**: Capture screenshots and analyze visual design, layout, and UX patterns using Gemini's vision capabilities.

**Implementation**:
- Use Playwright to capture full-page screenshots
- Send screenshot + metrics to Gemini 1.5 Flash/Pro (supports vision)
- Analyze: color contrast, visual hierarchy, mobile responsiveness, CTA prominence, whitespace usage

**Impact**: Unlocks insights impossible from metrics alone, such as "Primary CTA button has low contrast (fails WCAG AA)" or "Hero section occupies 85% of viewport, pushing content below fold."

---

### 2. Performance & Core Web Vitals Integration

**Objective**: Integrate Google Lighthouse API or PageSpeed Insights API for performance metrics.

**Implementation**:
- Run Lighthouse audit via Node.js or API
- Extract Core Web Vitals: LCP, FID, CLS, TTFB
- Include performance score in AI analysis context
- Generate recommendations like "LCP of 4.2s (slow) - optimize hero image (2.1MB)"

**Impact**: Provides objective performance data that correlates with user experience and SEO rankings. Critical for production-grade audits.

---

### 3. Multi-Page Crawling & Sitemap Analysis

**Objective**: Analyze entire websites, not just single pages.

**Implementation**:
- Parse sitemap.xml or crawl up to N pages
- Aggregate metrics across pages (avg word count, CTAs per page, alt text coverage)
- Identify patterns: "Homepage has 8 CTAs but product pages average only 1"
- Compare page types: landing pages vs. blog posts vs. product pages

**Impact**: Provides site-wide insights and identifies inconsistencies. Enables competitive analysis ("Competitor A averages 2,300 words per blog post vs. your 800").

---

### 4. Historical Tracking & Trend Analysis

**Objective**: Store audit results over time and track changes.

**Implementation**:
- Integrate lightweight database (Supabase, PostgreSQL, or SQLite)
- Store audit snapshots with timestamps
- Track metrics over time: "CTA count increased from 3 to 7 since last audit"
- Generate trend visualizations with Plotly/Altair
- Alert on regressions: "Alt text coverage dropped from 95% to 70%"

**Impact**: Enables before/after comparisons, ROI measurement, and regression detection. Critical for agencies or teams iterating on website improvements.

---

### Bonus: Additional Enhancements

- **Competitive Benchmarking**: Analyze competitor URLs and generate side-by-side comparisons
- **Custom Audit Templates**: Allow users to define custom metrics and analysis criteria
- **PDF/CSV Export**: Generate downloadable reports with branding
- **API Mode**: RESTful API for programmatic access (CI/CD integration)
- **Scheduled Audits**: Cron-based recurring audits with email notifications

---

## 🤝 Support

- **Google Gemini**: https://ai.google.dev
- **Streamlit**: https://docs.streamlit.io
- **Playwright**: https://playwright.dev/python
- **Docker**: https://docs.docker.com

---

## 📝 License

MIT License - Free for personal and commercial use

---

**Built with ❤️ for production deployment**

**Quick Deploy**: See [DEPLOY.md](DEPLOY.md) for step-by-step guides
