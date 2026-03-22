@echo off
REM Setup script for AI-Powered Website Audit Tool (Windows)

echo ==========================================
echo 🔍 Website Audit Tool - Setup Script
echo ==========================================

REM Check Python version
echo.
echo 📋 Checking Python version...
python --version

REM Create virtual environment
echo.
echo 🔧 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo.
echo ✅ Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo.
echo 📦 Installing Python packages...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Install Playwright browsers
echo.
echo 🌐 Installing Playwright browsers...
playwright install chromium

REM Create .env file if it doesn't exist
echo.
if not exist .env (
    echo 📝 Creating .env file...
    copy .env.example .env
    echo ⚠️  Please edit .env and add your GOOGLE_API_KEY
) else (
    echo ✅ .env file already exists
)

echo.
echo ==========================================
echo ✅ Setup complete!
echo ==========================================
echo.
echo Next steps:
echo 1. Edit .env and add your Google API key
echo 2. Test the setup: python test_setup.py
echo 3. Run the app: streamlit run app.py
echo.
pause
