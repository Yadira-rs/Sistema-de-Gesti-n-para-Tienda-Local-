# Actualización de Base de Datos - Clientes

## 📋 Descripción

Este script agrega campos separados para el nombre y apellidos de los clientes en la base de datos.

### Campos que se agregarán:
- `nombre_cliente` - Nombre del cliente
- `apellido_paterno` - Apellido paterno
- `apellido_materno` - Apellido materno

## 🚀 Cómo ejecutar la actualización

### Opción 1: Script Python (Recomendado)

1. Abre una terminal en la carpeta del proyecto
2. Ejecuta:
   ```bash
   python actualizar_base_datos_clientes.py
   ```
3. Confirma la actualización en el diálogo que aparece
4. ¡Listo! La base de datos se actualizará automáticamente

### Opción 2: Script SQL Manual

1. Abre tu gestor de base de datos (MySQL Workbench, phpMyAdmin, etc.)
2. Selecciona la base de datos `boutique_db`
3. Abre el archivo `actualizar_clientes.sql`
4. Ejecuta el script completo
5. Verifica los resultados con la consulta al final

## ✅ Qué hace el script

1. **Agrega nuevas columnas** a la tabla `clientes`:
   - `nombre_cliente`
   - `apellido_paterno`
   - `apellido_materno`

2. **Migra datos existentes**: 
   - Divide el campo `nombre` actual en las tres partes
   - Ejemplo: "Juan Pérez García" → 
     - Nombre: Juan
     - Apellido Paterno: Pérez
     - Apellido Materno: García

3. **Mantiene compatibilidad**:
   - El campo `nombre` original se conserva
   - No se pierden datos

## 🔍 Búsqueda mejorada

Después de la actualización, podrás buscar clientes por:
- ✅ Nombre
- ✅ Apellido Paterno
- ✅ Apellido Materno
- ✅ Teléfono
- ✅ Correo

## ⚠️ Importante

- **Haz un respaldo** de tu base de datos antes de ejecutar
- El script es seguro y no elimina datos
- Si ya ejecutaste el script antes, no hay problema en ejecutarlo de nuevo
- Los clientes nuevos deberán registrarse con los campos separados

## 📝 Ejemplo de uso

### Antes:
```
nombre: "María González López"
```

### Después:
```
nombre_cliente: "María"
apellido_paterno: "González"
apellido_materno: "López"
nombre: "María González López" (se mantiene)
```

## 🆘 Soporte

Si tienes problemas:
1. Verifica que la base de datos esté corriendo
2. Revisa el archivo `mysql_config.ini`
3. Ejecuta el script y revisa los mensajes en la consola
4. Si persiste el error, contacta al desarrollador

---

**Janet Rosa Bici - Sistema de Ventas**
