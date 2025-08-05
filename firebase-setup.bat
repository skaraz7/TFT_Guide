@echo off
echo Configurando Firebase en el proyecto TFT Guide...

echo.
echo 1. Instalando Firebase CLI...
npm install -g firebase-tools

echo.
echo 2. Iniciando sesion en Firebase...
firebase login

echo.
echo 3. Inicializando proyecto Firebase...
firebase init

echo.
echo Setup completado!
pause