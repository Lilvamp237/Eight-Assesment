#!/bin/bash

# Install Playwright browsers (bundled version)
# Note: Removed 'playwright install-deps' to avoid Debian package conflicts
# on Streamlit Cloud. Playwright's bundled Chromium has all needed libs.

echo "Installing Playwright browsers..."
playwright install chromium
echo "Playwright browsers installed successfully!"
