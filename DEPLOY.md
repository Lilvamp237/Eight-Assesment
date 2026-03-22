# 🚀 Production Deployment Guide

This Streamlit app can be deployed to multiple platforms. Choose the one that fits your needs.

---

## ⚡ Quick Deploy Options

### 1. Streamlit Cloud (Easiest - FREE)
**Best for**: Quick demos, no Docker needed
**Cost**: FREE unlimited public apps

```bash
# 1. Push code to GitHub
git add .
git commit -m "Ready for deployment"
git push

# 2. Go to https://share.streamlit.io
# 3. Connect your GitHub repository
# 4. Add secret: GOOGLE_API_KEY = your_key_here
# 5. Click Deploy!
```

**Done in 5 minutes!** ✅

---

### 2. Railway (Docker - Easy)
**Best for**: Production apps, auto-deploy from GitHub
**Cost**: $5/month (free trial available)

```bash
# Option A: Railway CLI
npm i -g @railway/cli
railway login
railway init
railway up

# Set environment variable
railway variables set GOOGLE_API_KEY=your_key_here

# Option B: GitHub Integration
# 1. Go to https://railway.app
# 2. Click "New Project" → "Deploy from GitHub"
# 3. Select your repository
# 4. Add GOOGLE_API_KEY to variables
# 5. Deploy automatically!
```

Railway will detect `railway.json` and deploy automatically.

---

### 3. Render (Docker - Easy)
**Best for**: Auto-deploy from GitHub, generous free tier
**Cost**: FREE tier available (spins down after 15min inactivity)

```bash
# Option A: render.yaml (Auto-detected)
# 1. Go to https://render.com
# 2. Click "New" → "Blueprint"
# 3. Connect GitHub repository
# 4. Render detects render.yaml automatically
# 5. Add GOOGLE_API_KEY in Render dashboard
# 6. Deploy!

# Option B: Manual Setup
# 1. Click "New" → "Web Service"
# 2. Connect repository
# 3. Select "Docker" as environment
# 4. Add GOOGLE_API_KEY to environment
# 5. Deploy!
```

---

### 4. Fly.io (Docker - Developer Friendly)
**Best for**: Global edge deployment, affordable
**Cost**: ~$5-10/month (3GB storage free)

```bash
# Install Fly CLI
# Windows: iwr https://fly.io/install.ps1 -useb | iex
# Mac: brew install flyctl
# Linux: curl -L https://fly.io/install.sh | sh

# Login and deploy
flyctl auth login
flyctl launch  # Creates fly.toml automatically

# Set secret
flyctl secrets set GOOGLE_API_KEY=your_key_here

# Deploy
flyctl deploy

# Your app will be live at: https://website-auditor.fly.dev
```

---

### 5. Google Cloud Run (Docker - Scalable)
**Best for**: Enterprise, high traffic, auto-scaling
**Cost**: FREE tier: 2M requests/month, then pay-per-use

```bash
# Prerequisites: Install Google Cloud SDK
# https://cloud.google.com/sdk/docs/install

# 1. Authenticate
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# 2. Build and push to Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/website-auditor

# 3. Deploy to Cloud Run
gcloud run deploy website-auditor \
  --image gcr.io/YOUR_PROJECT_ID/website-auditor \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_API_KEY=your_key_here \
  --port 8501

# Your app will be live at the URL shown in output
```

---

### 6. DigitalOcean App Platform
**Best for**: Simple production deployment
**Cost**: $5/month

```bash
# 1. Go to https://cloud.digitalocean.com/apps
# 2. Click "Create App"
# 3. Connect GitHub repository
# 4. Select "Dockerfile" as build method
# 5. Add environment variable: GOOGLE_API_KEY
# 6. Choose $5/month Basic plan
# 7. Deploy!
```

---

### 7. AWS Elastic Container Service (ECS)
**Best for**: Enterprise applications with AWS infrastructure
**Cost**: ~$15-30/month for Fargate

```bash
# Prerequisites: AWS CLI installed and configured
# https://aws.amazon.com/cli/

# 1. Create ECR repository
aws ecr create-repository --repository-name website-auditor

# 2. Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_AWS_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com

# 3. Build and push Docker image
docker build -t website-auditor .
docker tag website-auditor:latest YOUR_AWS_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/website-auditor:latest
docker push YOUR_AWS_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/website-auditor:latest

# 4. Create ECS service via AWS Console
# - Task definition: Use pushed image
# - Set environment variable: GOOGLE_API_KEY
# - Configure load balancer and auto-scaling
```

---

## 🐳 Local Docker Testing

Before deploying, test locally:

```bash
# 1. Build Docker image
docker build -t website-auditor .

# 2. Run container
docker run -p 8501:8501 -e GOOGLE_API_KEY=your_key_here website-auditor

# 3. Access at http://localhost:8501
```

Or use Docker Compose:

```bash
# 1. Create .env file with GOOGLE_API_KEY
echo "GOOGLE_API_KEY=your_key_here" > .env

# 2. Start services
docker-compose up -d

# 3. Access at http://localhost:8501

# 4. Stop services
docker-compose down
```

---

## 📊 Platform Comparison

| Platform | Pros | Cons | Cost | Best For |
|----------|------|------|------|----------|
| **Streamlit Cloud** | ✅ Easiest<br>✅ FREE<br>✅ No Docker | ❌ Limited resources<br>❌ Public only | FREE | Demos, testing |
| **Railway** | ✅ Auto-deploy<br>✅ Easy setup<br>✅ Good pricing | ❌ Newer platform | $5/mo | Startups, MVP |
| **Render** | ✅ FREE tier<br>✅ Auto-deploy<br>✅ Easy | ❌ Spins down on free | Free-$7/mo | Side projects |
| **Fly.io** | ✅ Global edge<br>✅ Fast<br>✅ Dev-friendly | ❌ Learning curve | $5-10/mo | Developers |
| **Google Cloud Run** | ✅ Auto-scale<br>✅ Pay-per-use<br>✅ Reliable | ❌ Setup complexity | $5-20/mo | Production |
| **DigitalOcean** | ✅ Simple<br>✅ Predictable pricing | ❌ Manual scaling | $5/mo | Production |
| **AWS ECS** | ✅ Enterprise<br>✅ Full control | ❌ Complex setup<br>❌ Expensive | $15-30/mo | Enterprise |

---

## 🎯 Recommended Path

### For Assignment Demo:
👉 **Streamlit Cloud** - Free, fast, no Docker needed

### For Portfolio/Resume:
👉 **Railway or Render** - Shows Docker skills, production-ready

### For Learning Cloud:
👉 **Google Cloud Run or Fly.io** - Industry-standard platforms

---

## 🔒 Security Checklist

Before deploying:

- [ ] ✅ `.env` file in `.gitignore`
- [ ] ✅ API key set as environment variable (not hardcoded)
- [ ] ✅ Dockerfile doesn't expose secrets
- [ ] ✅ Health check endpoint working
- [ ] ✅ HTTPS enabled (most platforms do this automatically)

---

## 🐛 Troubleshooting

### Issue: "Port already in use"
```bash
# Change port in docker-compose.yml or use different port
docker run -p 8502:8501 -e GOOGLE_API_KEY=key website-auditor
```

### Issue: "Memory limit exceeded"
```bash
# Increase memory in platform settings or Dockerfile
# Railway/Render: Upgrade to higher tier
# Docker: docker run -m 1g website-auditor
```

### Issue: "Playwright browser not found"
```bash
# Ensure Dockerfile has playwright install steps (already included)
RUN playwright install chromium
RUN playwright install-deps chromium
```

### Issue: "Health check failing"
```bash
# Verify Streamlit is running on correct port
# Check logs: docker logs <container_id>
# Ensure /_stcore/health endpoint is accessible
```

---

## 🎉 Next Steps After Deployment

1. **Test the deployed app** with multiple URLs
2. **Monitor performance** using platform dashboards
3. **Set up alerts** for downtime or errors
4. **Share the URL** for feedback
5. **Consider adding**:
   - Rate limiting
   - Caching layer
   - Analytics
   - Export to PDF feature

---

## ❓ Need Help?

- **Streamlit Cloud**: https://docs.streamlit.io/streamlit-community-cloud
- **Railway**: https://docs.railway.app
- **Render**: https://render.com/docs
- **Fly.io**: https://fly.io/docs
- **Google Cloud**: https://cloud.google.com/run/docs

---

**Quick Start**: For fastest deployment, use Streamlit Cloud. For production with Docker, use Railway or Render.
