@echo off
title CareerPilot AI - Backend
echo ===================================================
echo   Starting CareerPilot AI Backend on port 8000
echo ===================================================
cd /d "%~dp0backend"
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
pause

