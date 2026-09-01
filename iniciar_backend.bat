@echo off
title PrevCalc INSS - Servidor Back-end FastAPI
cls
echo ======================================================================
echo           PREVCALC INSS - INICIANDO BACK-END FASTAPI
echo ======================================================================
echo.
cd /d "%~dp0"
set PYTHONPATH=backend
python -m uvicorn app.main:app --reload --port 8000
pause
