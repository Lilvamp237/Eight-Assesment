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

# 5. Expose port and setup health check
EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# 6. Run the application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]