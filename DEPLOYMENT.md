# 🚀 Deployment & Usage Guide

## Quick Start (2 minutes)

### Windows
```bash
# Run setup script
setup.bat

# Edit .env file with your API key
notepad .env

# Test the setup
python test_setup.py

# Launch the app
streamlit run app.py
```

### Mac/Linux
```bash
# Make setup script executable
chmod +x setup.sh

# Run setup
./setup.sh

# Edit .env file with your API key
nano .env  # or use your preferred editor

# Test the setup
python test_setup.py

# Launch the app
streamlit run app.py
```

## Getting Your Google API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and paste it in your `.env` file:
   ```
   GOOGLE_API_KEY=AIzaSyC...your_key_here
   ```

## Testing Different Websites

```bash
# Test with a custom URL
python test_setup.py https://www.example.com
```

Good test URLs:
- `https://example.com` - Simple static page
- `https://stripe.com` - Modern SaaS site
- `https://github.com` - Complex web app
- Your own website!

## Troubleshooting

### Issue: "Playwright browser not found"
```bash
# Reinstall Playwright browsers
playwright install chromium
```

### Issue: "API key not found"
Check that:
1. `.env` file exists in project root
2. File contains: `GOOGLE_API_KEY=your_actual_key`
3. No spaces around the `=` sign
4. Key starts with `AIza...`

### Issue: "Page load timeout"
The website might be slow or blocking bots. Try:
1. Increasing timeout in `scraper.py`:
   ```python
   scraper = WebsiteScraper(timeout=60000)  # 60 seconds
   ```
2. Testing with a different URL

### Issue: "Module not found"
Make sure virtual environment is activated:
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

## Performance Tips

### Faster Analysis
Use Gemini Flash (default) for speed, or upgrade to Pro for higher quality:

```python
# In analyzer.py
analyst = AuditAnalyst(model_name="gemini-1.5-pro")  # Slower but better
```

### Batch Processing
To audit multiple URLs, modify `test_setup.py`:

```python
urls = [
    "https://example.com",
    "https://another-site.com",
    "https://your-site.com"
]

for url in urls:
    print(f"\n{'='*60}")
    print(f"Auditing: {url}")
    test_audit(url)
```

## Sharing Your Audit Tool

### Option 1: Streamlit Cloud (Free)
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo
4. Add `GOOGLE_API_KEY` in Streamlit secrets

### Option 2: Docker (Advanced)
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt && playwright install chromium

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501"]
```

Build and run:
```bash
docker build -t website-auditor .
docker run -p 8501:8501 -e GOOGLE_API_KEY=your_key website-auditor
```

## Cost Estimation

**Gemini 1.5 Flash Pricing** (as of 2024):
- Input: $0.075 per 1M tokens
- Output: $0.30 per 1M tokens

**Average audit cost**:
- ~1,000 tokens per audit
- **Cost per audit**: < $0.001 (less than a tenth of a cent)
- **100 audits**: ~$0.10

**Free tier**: 15 requests per minute, plenty for testing!

## Advanced Configuration

### Custom CTA Patterns
Edit `scraper.py` line 75 to detect your own CTAs:

```python
cta_keywords = [
    'buy now', 'get started', 'sign up',
    'custom keyword', 'your cta text'
]
```

### Adjust AI Temperature
Lower = more consistent, Higher = more creative

```python
# In analyzer.py
self.llm = ChatGoogleGenerativeAI(
    model=model_name,
    temperature=0.1,  # More deterministic (0.0 - 2.0)
)
```

### Change System Prompt
Modify `SYSTEM_PROMPT` in `analyzer.py` to customize AI behavior:

```python
SYSTEM_PROMPT = """You are a [your custom role]...
Focus on [your specific areas]...
"""
```

## Production Checklist

Before deploying to production:

- [ ] Add rate limiting for API calls
- [ ] Implement caching (avoid re-scraping same URL)
- [ ] Add user authentication if needed
- [ ] Set up error monitoring (Sentry, etc.)
- [ ] Configure HTTPS
- [ ] Add database for storing audit history
- [ ] Implement export to PDF/CSV
- [ ] Add more comprehensive error messages
- [ ] Set up CI/CD pipeline
- [ ] Add unit tests

## Security Notes

⚠️ **Important**:
- Never commit `.env` file to git (already in `.gitignore`)
- Rotate API keys regularly
- Use environment variables in production
- Don't expose API keys in client-side code
- Consider rate limiting to prevent abuse

## Support & Resources

- **Streamlit Docs**: https://docs.streamlit.io
- **LangChain Docs**: https://python.langchain.com
- **Gemini API**: https://ai.google.dev
- **Playwright**: https://playwright.dev/python/

## License

MIT License - Free for commercial and personal use.

---

**Questions?** Open an issue or check the README.md for more details.
