#!/bin/bash

# Install Playwright browsers and dependencies
playwright install-deps
playwright install chromium

echo "Playwright setup completed successfully!"
