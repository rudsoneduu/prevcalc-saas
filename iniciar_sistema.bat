@echo off
title PrevCalc INSS - Sistema Web (1978-2026)
cls
echo ======================================================================
echo           PREVCALC INSS - INICIALIZADOR AUTOMATICO DO SISTEMA
echo ======================================================================
echo.

cd /d "%~dp0"

echo [1/3] Verificando se o Next.js esta instalado no Front-end...
if exist "frontend\node_modules\.bin\next.cmd" goto NODE_OK

echo Instalando pacotes npm no frontend (isso pode levar 1 a 2 minutos)...
cd frontend
call npm install
cd ..

:NODE_OK
echo Dependencias do Front-end OK.

echo.
echo [2/3] Iniciando o Servidor Back-end FastAPI em porta 8000...
start "Backend FastAPI PrevCalc" cmd /k "set PYTHONPATH=backend&& python -m uvicorn app.main:app --reload --port 8000"

echo.
echo [3/3] Iniciando o Servidor Front-end Next.js em porta 3000...
start "Frontend Next.js PrevCalc" cmd /k "cd frontend && npm run dev"

echo.
echo ======================================================================
echo  Sistema inicializado com sucesso!
echo  - Back-end API: http://localhost:8000/docs
echo  - Front-end Web: http://localhost:3000
echo ======================================================================
echo.
ping 127.0.0.1 -n 3 >nul
start http://localhost:3000
exit
