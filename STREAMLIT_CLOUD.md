# 🚀 Streamlit Cloud Deployment Guide

## Quick Deploy (5 Minutes)

### Step 1: Prepare Your Repository

```bash
# Ensure all changes are committed
git add .
git commit -m "Ready for Streamlit Cloud deployment"
git push origin main
```

### Step 2: Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud**:
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account

2. **Create New App**:
   - Click "New app" button
   - Select your repository: `Eight-Assesment`
   - Branch: `main`
   - Main file path: `app.py`

3. **Configure Secrets**:
   - Click "Advanced settings"
   - Go to "Secrets" section
   - Paste the following (replace with your actual key):

   ```toml
   GOOGLE_API_KEY = "AIzaSyC...your_actual_key_here"
   ```

4. **Deploy**:
   - Click "Deploy!"
   - Wait 2-3 minutes for deployment
   - Your app will be live at: `https://your-app-name.streamlit.app`

---

## Troubleshooting

### Issue: "Playwright browser not found"

**This issue has been fixed** in the latest version. The app now uses system Chromium installed via `packages.txt`.

If you still see errors:

1. **Verify `packages.txt` contains**:
   ```
   chromium
   chromium-driver
   libglib2.0-0
   libnss3
   libnspr4
   libdbus-1-3
   libatk1.0-0
   libatk-bridge2.0-0
   libcups2
   libdrm2
   libxkbcommon0
   libxcomposite1
   libxdamage1
   libxfixes3
   libxrandr2
   libgbm1
   libpango-1.0-0
   libcairo2
   libasound2
   ```

2. **Verify `scraper.py` uses system Chromium**:
   The code automatically detects and uses system Chromium on Streamlit Cloud.

3. **Reboot the app**:
   - Go to Streamlit Cloud dashboard
   - Click "Reboot app"
   - Wait 2-3 minutes for rebuild

4. **Check Playwright version** in `requirements.txt`:
   ```
   playwright==1.41.0
   ```

### Issue: "API key not found"

1. Go to app settings → Secrets
2. Ensure format is correct (no quotes around the key in TOML):
   ```toml
   GOOGLE_API_KEY = "your_key_here"
   ```
3. Reboot the app

### Issue: "Module not found"

1. Check `requirements.txt` has all dependencies
2. Reboot app from dashboard
3. Check logs for specific missing module

---

## App Management

### Viewing Logs
- Click on your app in Streamlit Cloud dashboard
- Click "Manage app" → "Logs"
- Real-time logs will appear

### Updating the App
```bash
# Make changes locally
git add .
git commit -m "Update feature X"
git push

# Streamlit Cloud auto-deploys on push
# Wait 1-2 minutes for rebuild
```

### Custom Domain (Optional)
- Go to app settings
- Click "Custom domain"
- Follow DNS configuration instructions

---

## Performance Tips

1. **Cold Start**: First request takes ~3-5s (Playwright loading)
2. **Concurrent Users**: Streamlit Cloud free tier supports light traffic
3. **Rate Limiting**: Consider adding request throttling for production

---

## Alternative: Local Docker Testing

Before deploying, test with Docker:

```bash
# Build and run
docker-compose up -d

# Access at http://localhost:8501

# Stop
docker-compose down
```

---

## Cost

**Streamlit Cloud Free Tier**:
- ✅ Unlimited public apps
- ✅ Auto-deploy from GitHub
- ✅ HTTPS included
- ✅ 1GB RAM, 1 CPU core
- ✅ Community support

**Paid Tier** ($20/month):
- Private apps
- More resources
- Priority support

---

## Next Steps After Deployment

1. ✅ Test the live app with multiple URLs
2. ✅ Share the link for feedback
3. ✅ Monitor usage in Streamlit Cloud dashboard
4. ✅ Add app to your portfolio/resume

---

**Your app will be live at**: `https://[your-app-name].streamlit.app`

**Need help?** Visit [Streamlit Community](https://discuss.streamlit.io/)
