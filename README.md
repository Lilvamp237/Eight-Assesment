# 🔍 AI-Powered Website Audit Tool

A lightweight, production-ready tool that combines **factual web scraping** with **AI-powered analysis** to deliver comprehensive website audits. Built with Streamlit, Playwright, and Google Gemini.

## 🎯 Features

- **Factual Metric Extraction**: Uses Playwright + BeautifulSoup to extract real data:
  - Word count, heading distribution (H1-H3)
  - CTA identification and counting
  - Internal vs. external link analysis
  - Image count and alt text accessibility audit
  - SEO metadata (title, description)

- **AI-Powered Insights**: LangChain + Gemini generates:
  - SEO analysis grounded in actual metrics
  - Messaging and content depth evaluation
  - CTA effectiveness assessment
  - UX and accessibility concerns
  - 3-5 prioritized, actionable recommendations

- **Full Transparency**: Prompt logging shows:
  - System prompt
  - User prompt with metrics
  - Structured input (PageMetrics)
  - Raw model output (AuditReport)

## 📁 Project Structure

```
.
├── models.py       # Pydantic models (PageMetrics, AuditReport)
├── logger.py       # Prompt logging utility
├── scraper.py      # WebsiteScraper (Playwright + BeautifulSoup)
├── analyzer.py     # AuditAnalyst (LangChain + Gemini)
├── app.py          # Streamlit UI
├── requirements.txt
└── .env.example
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python packages
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### 2. Set Up API Key

**Option A: Environment Variable (Recommended)**
```bash
# Copy .env.example to .env
cp .env.example .env

# Edit .env and add your Google API key
GOOGLE_API_KEY=your_actual_api_key_here
```

**Option B: Streamlit Sidebar**
- Enter your API key directly in the sidebar when running the app

**Getting a Google API Key:**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Enable the Gemini API

### 3. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 Usage

1. **Enter URL**: Type the website URL you want to audit
2. **Configure API Key**: Add your Google API key (sidebar or .env)
3. **Run Audit**: Click "🚀 Run Audit"
4. **Review Results**:
   - **Left Column**: Factual metrics extracted from the page
   - **Right Column**: AI insights grounded in those metrics
   - **Bottom Section**: Prioritized recommendations
5. **Inspect Reasoning**: Expand "Prompt Logs / Reasoning Trace" to see:
   - Complete system prompt
   - User prompt with all metrics
   - Raw AI output

## 🛠️ Technical Architecture

### Separation of Concerns

```
User Input (URL)
    ↓
WebsiteScraper (Playwright/BS4)
    ↓
PageMetrics (Pydantic)
    ↓
AuditAnalyst (LangChain + Gemini)
    ↓
AuditReport (Pydantic)
    ↓
Streamlit UI Display
```

### Key Design Decisions

1. **Playwright over requests**: Handles JavaScript-heavy sites
2. **Pydantic validation**: Ensures structured, type-safe data
3. **Low AI temperature (0.3)**: Reduces hallucination, increases consistency
4. **Explicit grounding prompt**: Forces AI to cite specific metrics
5. **Session-based logging**: Full transparency without file I/O

## 🧪 Example Output

**Input URL**: `https://example.com`

**Factual Metrics**:
- 1,250 words, 1 H1, 5 H2s, 8 H3s
- 3 CTAs, 15 internal links, 5 external links
- 10 images, 20% missing alt text

**AI Insights**:
- "With only 3 CTAs across 1,250 words (1 per 417 words), conversion opportunities are limited..."
- "20% of images (2/10) lack alt text, creating accessibility barriers..."

**Recommendations**:
1. Add alt text to 2 images immediately
2. Increase CTAs from 3 to 6-8 (target 1 per 200-250 words)
3. Shorten meta description by 10 characters

## 🔧 Customization

### Adjusting CTA Detection

Edit `scraper.py` → `_count_ctas()` to modify CTA keyword patterns:

```python
cta_keywords = [
    'sign up', 'buy now', 'learn more',  # Add your keywords
]
```

### Changing AI Model

Edit `analyzer.py` → `__init__()`:

```python
self.llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",  # Use Pro for higher quality
    temperature=0.1,          # Lower = more deterministic
)
```

### Custom System Prompt

Modify `SYSTEM_PROMPT` in `analyzer.py` to adjust AI behavior.

## 📊 Metrics Collected

| Category | Metrics |
|----------|---------|
| **Content** | Word count, H1/H2/H3 counts |
| **Conversion** | CTA count (buttons + action links) |
| **Links** | Internal links, External links |
| **Media** | Image count, % missing alt text |
| **SEO** | Meta title, Meta description |

## 🤝 Contributing

This is a 24-hour assignment project. For production use:
- Add error handling for edge cases
- Implement rate limiting
- Add caching for repeated audits
- Support batch URL processing
- Add export to PDF/CSV

## 📝 License

MIT License - feel free to use for learning or commercial purposes.

## 🙋 Support

- **Google Gemini Issues**: Check [Google AI documentation](https://ai.google.dev/)
- **Playwright Issues**: See [Playwright docs](https://playwright.dev/python/)
- **Streamlit Issues**: Visit [Streamlit community](https://discuss.streamlit.io/)

## ⚡ Performance Notes

- **Average audit time**: 5-15 seconds (depends on page size and AI response time)
- **Playwright timeout**: 30 seconds (configurable in `scraper.py`)
- **Token usage**: ~500-1000 tokens per audit (Gemini Flash is very cost-effective)

---

**Built with ❤️ for the Eight Sleep AI Engineering Assessment**
