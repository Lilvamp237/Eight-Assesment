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

### Production Deployment

See **[DEPLOY.md](DEPLOY.md)** for complete deployment guides to:

- ⚡ **Streamlit Cloud** (FREE, easiest)
- 🚂 **Railway** ($5/mo, auto-deploy)
- 🎨 **Render** (FREE tier available)
- ✈️ **Fly.io** ($5-10/mo, global edge)
- ☁️ **Google Cloud Run** (auto-scale, pay-per-use)
- 🌊 **DigitalOcean** ($5/mo, simple)
- 📦 **AWS ECS** (enterprise)

**Quick recommendation**:
- **Demo**: Use Streamlit Cloud (free, 5-min setup)
- **Production**: Use Railway or Render (Docker, easy)

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

- [ ] Google API key obtained
- [ ] `.env` file created locally
- [ ] Tested locally with `streamlit run app.py`
- [ ] Tested with Docker: `docker-compose up`
- [ ] Chose deployment platform (see DEPLOY.md)
- [ ] Set `GOOGLE_API_KEY` environment variable on platform
- [ ] Deployed and tested live URL
- [ ] Verified health check endpoint works

---

## 📚 Documentation

- **[DEPLOY.md](DEPLOY.md)** - Complete deployment guide for all platforms
- **[README.md](README.md)** - This file (overview and quick start)

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
