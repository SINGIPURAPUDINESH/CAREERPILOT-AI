@echo off
title CareerPilot AI Launcher
echo ===================================================
echo   Launching CareerPilot AI (Backend + Frontend)
echo ===================================================

echo Starting Backend on http://localhost:8000...
start "CareerPilot AI - Backend" cmd /k "cd /d %~dp0backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

echo Starting Frontend on http://localhost:3000...
start "CareerPilot AI - Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo Both servers are starting up in separate terminal windows!
echo - Frontend: http://localhost:3000
echo - Backend:  http://localhost:8000/docs
echo.
pause

