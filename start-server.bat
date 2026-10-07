@echo off
title PrintBai Local Server
cd /d "D:\PrintBai"
echo ========================================================
echo   Starting PrintBai Local Web Server (Port 8000)...
echo ========================================================
echo.
echo Website URL: http://localhost:8000
echo.
echo Press Ctrl+C in this window to stop the server when done.
echo.
py -m http.server 8000
pause
