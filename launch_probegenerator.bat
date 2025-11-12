@echo off
REM ProbeGenerator Launcher for Windows

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0

REM Navigate to the web_streamlit directory
cd /d "%SCRIPT_DIR%web_streamlit"

REM Check if streamlit is installed
streamlit --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Streamlit is not installed. Installing required packages...
    pip install -r requirements.txt
)

REM Launch Streamlit
echo Starting ProbeGenerator...
echo The app will open in your browser automatically
echo.
echo Press Ctrl+C to stop the server
echo.

streamlit run app.py --browser.gatherUsageStats false

REM Keep window open if there's an error
pause
