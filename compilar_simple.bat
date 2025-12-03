@echo off
echo ======================================================================
echo COMPILANDO JANET ROSA BICI
echo ======================================================================
echo.

echo Limpiando compilaciones anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo Limpieza completada
echo.

echo Compilando con PyInstaller...
echo Esto puede tardar varios minutos...
echo.

python -m PyInstaller --onefile --windowed --name=JanetRosaBici --add-data=controllers;controllers --add-data=database;database --add-data=views;views --hidden-import=PIL._tkinter_finder --hidden-import=mysql.connector --hidden-import=customtkinter --hidden-import=openpyxl app.py

echo.
echo Copiando archivos necesarios...
if exist logo.png copy logo.png dist\
if exist mysql_config.ini copy mysql_config.ini dist\
if exist README.md copy README.md dist\
if exist LEEME_PRIMERO.txt copy LEEME_PRIMERO.txt dist\

echo.
echo ======================================================================
echo COMPILACION COMPLETADA
echo ======================================================================
echo.
echo El ejecutable esta en: dist\JanetRosaBici.exe
echo.
pause
