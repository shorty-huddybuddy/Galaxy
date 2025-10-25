@echo off
echo ============================================
echo Hand Gesture Solar System - Quick Start
echo ============================================
echo.

echo [1/3] Activating virtual environment...
call handgasture\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Could not activate virtual environment
    pause
    exit /b 1
)

echo [2/3] Checking if server is already running...
netstat -ano | findstr :5000 >nul
if %errorlevel%==0 (
    echo WARNING: Port 5000 is already in use!
    echo Please close the other server first.
    pause
    exit /b 1
)

echo [3/3] Starting gesture server...
echo.
echo ============================================
echo Server will start shortly...
echo Then open: http://localhost:5000
echo Press Ctrl+C to stop the server
echo ============================================
echo.
python backend\gesture_server.py

pause
