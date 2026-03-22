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

# 3. Install Playwright AND its dependencies
# We run apt-get update here so install-deps has the metadata it needs
RUN apt-get update && \
    playwright install chromium && \
    playwright install-deps chromium && \
    rm -rf /var/lib/apt/lists/*

# 4. Copy application code
COPY . .

# 5. Expose default port (Railway will override with dynamic PORT)
EXPOSE 8501

# 6. Run the application (Railway will inject $PORT at runtime)
CMD streamlit run app.py --server.port=${PORT:-8501} --server.address=0.0.0.0