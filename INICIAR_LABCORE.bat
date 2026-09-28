@echo off
setlocal
cd /d "%~dp0"
title LabCore - Laboratorio de Ciencias

if not exist ".venv\Scripts\python.exe" (
  echo [LabCore] Criando o ambiente virtual...
  py -3.11 -m venv .venv >nul 2>&1
  if errorlevel 1 py -3 -m venv .venv
  if errorlevel 1 (
    echo ERRO: instale o Python 3.11 ou mais recente e marque Add Python to PATH.
    pause
    exit /b 1
  )
)

".venv\Scripts\python.exe" -c "import django" >nul 2>&1
if errorlevel 1 (
  echo [LabCore] Instalando o Django no ambiente virtual...
  ".venv\Scripts\python.exe" -m pip install -r requirements.txt
  if errorlevel 1 (
    echo ERRO: nao foi possivel instalar as dependencias. Confira a internet.
    pause
    exit /b 1
  )
)

echo [LabCore] Abrindo o jogo...
".venv\Scripts\python.exe" main.py
if errorlevel 1 (
  echo [LabCore] Ocorreu um erro. Copie a mensagem acima para diagnostico.
  pause
)
endlocal
