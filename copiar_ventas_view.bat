@echo off
del /F /Q views\ventas_view.py 2>nul
copy /Y views\ventas_view_nuevo.py views\ventas_view.py
echo Archivo copiado exitosamente
pause
