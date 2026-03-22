# 🚀 Quick Reference Card

## Setup (5 minutes)

### Option 1: Automated Setup (Recommended)
```bash
# Windows
setup.bat

# Mac/Linux
chmod +x setup.sh && ./setup.sh
```

### Option 2: Manual Setup
```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt
playwright install chromium

# 3. Configure API key
cp .env.example .env
# Edit .env and add: GOOGLE_API_KEY=your_key_here
```

## Usage

### Test Installation
```bash
python test_setup.py
```

### Run Application
```bash
streamlit run app.py
```

### Command Line Test
```bash
python test_setup.py https://your-website.com
```

## Project Structure

```
Eight-Assesment/
├── 📦 CORE FILES (Required)
│   ├── models.py          # Pydantic models (PageMetrics, AuditReport)
│   ├── logger.py          # Prompt logging utility
│   ├── scraper.py         # WebsiteScraper (Playwright + BS4)
│   ├── analyzer.py        # AuditAnalyst (LangChain + Gemini)
│   └── app.py             # Streamlit UI
│
├── 🔧 CONFIGURATION
│   ├── requirements.txt   # Python dependencies
│   ├── .env.example       # Environment template
│   └── .gitignore         # Git exclusions
│
├── 📚 DOCUMENTATION
│   ├── README.md          # Main documentation
│   ├── DEPLOYMENT.md      # Setup & deployment guide
│   └── PROJECT_SUMMARY.md # Architecture & features
│
└── 🛠️ UTILITIES
    ├── setup.sh           # Linux/Mac setup script
    ├── setup.bat          # Windows setup script
    └── test_setup.py      # Validation script
```

## Key Features

### 🎯 Factual Metrics Extracted
- ✅ Word count
- ✅ H1, H2, H3 counts
- ✅ CTA detection (buttons + action links)
- ✅ Internal vs. external links
- ✅ Image count + missing alt text %
- ✅ Meta title & description

### 🤖 AI Insights Generated
- ✅ SEO analysis (grounded in heading structure, meta tags)
- ✅ Messaging evaluation (based on word count, clarity)
- ✅ CTA effectiveness (tied to conversion metrics)
- ✅ Content depth assessment (heading hierarchy)
- ✅ UX concerns (accessibility, navigation)
- ✅ 3-5 prioritized recommendations (specific, actionable)

### 📊 UI Components
- ✅ Clean URL input
- ✅ Side-by-side display (Metrics | Insights)
- ✅ Visual metric cards
- ✅ Styled insight boxes
- ✅ Highlighted recommendations
- ✅ Expandable prompt logs (system prompt, user prompt, raw output)

## Common Commands

| Task | Command |
|------|---------|
| **Activate venv** | `source venv/bin/activate` (Win: `venv\Scripts\activate`) |
| **Install deps** | `pip install -r requirements.txt` |
| **Install browsers** | `playwright install chromium` |
| **Test setup** | `python test_setup.py` |
| **Run app** | `streamlit run app.py` |
| **Test custom URL** | `python test_setup.py https://example.com` |
| **Clear logs** | Click "Clear Logs" in sidebar |

## Environment Variables

```bash
# .env file
GOOGLE_API_KEY=AIzaSyC...your_key_here
```

Get your key: [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)

## Troubleshooting

| Problem | Solution |
|---------|----------|
| **Module not found** | Activate virtual environment |
| **Playwright error** | Run `playwright install chromium` |
| **API key error** | Check `.env` file exists and has correct format |
| **Timeout error** | Increase timeout in `scraper.py` or try different URL |
| **No output** | Check prompt logs for API errors |

## Example Output

```
📊 Factual Metrics          🤖 AI Insights
─────────────────          ────────────────
Words: 1,250               "With 1,250 words distributed
H1s: 1                     across 1 H1, 5 H2s, and 8 H3s,
H2s: 5                     the content shows strong
H3s: 8                     hierarchical structure..."
CTAs: 3
Images: 10 (20% no alt)    "Critical: 20% of images (2/10)
                           lack alt text..."

✨ Recommendations
─────────────────
#1 Add alt text to 2 images immediately (accessibility)
#2 Increase CTAs from 3 to 6-8 (target 1 per 200 words)
#3 Shorten meta description by 10 characters
```

## Cost Per Audit

- **Gemini Flash**: ~$0.0005 per audit (half a cent)
- **Free tier**: 15 requests/minute
- **100 audits**: ~$0.10

## Customization

### Change AI Model
```python
# analyzer.py, line 54
analyst = AuditAnalyst(model_name="gemini-1.5-pro")
```

### Adjust Temperature
```python
# analyzer.py, line 57
temperature=0.1  # More deterministic (0.0 - 2.0)
```

### Add CTA Keywords
```python
# scraper.py, line 75
cta_keywords = ['buy now', 'sign up', 'your custom keyword']
```

## Production Deployment

### Streamlit Cloud
```bash
1. Push to GitHub
2. Go to share.streamlit.io
3. Connect repo
4. Add GOOGLE_API_KEY to secrets
```

### Docker
```bash
docker build -t website-auditor .
docker run -p 8501:8501 -e GOOGLE_API_KEY=key website-auditor
```

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | Streamlit |
| **Scraping** | Playwright + BeautifulSoup4 |
| **AI** | LangChain + Google Gemini 1.5 Flash |
| **Validation** | Pydantic v2 |
| **Language** | Python 3.11+ |

## Support

- 📖 **Full docs**: See README.md
- 🚀 **Deployment**: See DEPLOYMENT.md
- 🏗️ **Architecture**: See PROJECT_SUMMARY.md

---

**Assignment Status**: ✅ Complete and ready for review
