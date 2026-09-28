@echo off
setlocal
cd /d "%~dp0"
title LabCore - Aplicar revisao ao repositorio

echo ===========================================================
echo   INSTALAR A REVISAO DO LABCORE NA SUA PASTA ORIGINAL
echo ===========================================================
echo.
echo A pasta deve ser aquela que ja tem main.py e static\assets.
echo Exemplo: C:\Users\SEU_USUARIO\labcore
echo.
set /p DEST=Digite ou cole o caminho COMPLETO da pasta labcore: 
if "%DEST%"=="" (
  echo Nenhuma pasta informada.
  pause
  exit /b 1
)

py -3 INSTALAR_NO_REPO.py "%DEST%"
if errorlevel 1 (
  python INSTALAR_NO_REPO.py "%DEST%"
)
if errorlevel 1 (
  echo Falha na instalacao. Confira o caminho informado e a mensagem acima.
  pause
  exit /b 1
)
echo.
echo Pronto! Entre na pasta original e execute INICIAR_LABCORE.bat.
pause
endlocal
