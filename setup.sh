#!/bin/bash

# Install Playwright browsers if not already installed
# This script runs before the Streamlit app starts on Streamlit Cloud

echo "Installing Playwright browsers..."
playwright install chromium
playwright install-deps chromium
echo "Playwright browsers installed successfully!"
