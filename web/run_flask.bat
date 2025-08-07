@echo off
echo ============================================
echo  DFIR Log Sorter - Flask Web Application
echo ============================================
echo.
echo Starting Flask development server...
echo.

REM Check if Flask is installed
python -c "import flask" 2>nul
if errorlevel 1 (
    echo Error: Flask is not installed!
    echo.
    echo Installing Flask and dependencies...
    pip install -r requirements.txt
    echo.
)

REM Create logs directory if it doesn't exist
if not exist "logs" mkdir logs

echo Flask application starting...
echo.
echo ✓ Logs directory ready
echo ✓ Dependencies checked
echo.
echo ==========================================
echo  Your DFIR Log Sorter is now running!
echo ==========================================
echo.
echo 🌐 Open your browser and go to:
echo    http://localhost:5000
echo.
echo 📁 Log files will be saved in: ./logs/
echo.
echo Press Ctrl+C to stop the server
echo ==========================================
echo.

REM Start Flask application
python app.py

echo.
echo Flask server stopped.
pause
