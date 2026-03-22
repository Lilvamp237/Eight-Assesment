FROM python:3.11-slim

# 1. Install initial tools and curl for the health check
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Install Playwright dependencies manually and then Playwright
# Install core dependencies needed for Playwright on Debian Trixie
RUN apt-get update && apt-get install -y \
    libnss3 \
    libatk-bridge2.0-0 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libxtst6 \
    libasound2 \
    libpangocairo-1.0-0 \
    libatk1.0-0 \
    libcairo-gobject2 \
    libgtk-3-0 \
    libgdk-pixbuf2.0-0 \
    fonts-liberation \
    fonts-unifont \
    && rm -rf /var/lib/apt/lists/*

# Install Playwright chromium browser
RUN playwright install chromium

# 4. Copy application code
COPY . .

# 5. Expose default port (Railway will override with dynamic PORT)
EXPOSE 8501

# 6. Run the application (Railway will inject $PORT at runtime)
CMD streamlit run app.py --server.port=${PORT:-8501} --server.address=0.0.0.0