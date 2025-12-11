@echo off
echo Verificando si el nuevo logo existe...
if exist "nuevo_logo_janet_rosa.png" (
    echo ✓ Nuevo logo encontrado
    echo Actualizando logo...
    python actualizar_logo_nuevo.py
) else (
    echo ❌ No se encuentra el nuevo logo
    echo.
    echo INSTRUCCIONES:
    echo 1. Guarde la imagen del logo como "nuevo_logo_janet_rosa.png"
    echo 2. Coloquela en esta carpeta
    echo 3. Ejecute este archivo nuevamente
)
pause