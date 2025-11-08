# 


#  Sistema de Gestión para Tienda Local (boutique)

**Proyecto Integrador I – Universidad Tecnológica de Durango**

Desarrollado por:  
- Santiago Santos Iris Yadira  
- Robles Danna Michell  
- Medina Lucía  
- Reyes Arce Cindy Alejandra  
- Benítez Montelongo Owen Asaf  

 Grupo: 4°B – Tecnologías de la Información

---

##  Descripción del proyecto

El **Sistema de Gestión para Tienda Local** es una aplicación de escritorio desarrollada en **Python** con **Tkinter** y **MySQL**, diseñada para automatizar las operaciones principales de una tienda que vende productos variados (ropa, artículos de cuidado personal, dulces, etc.).

El sistema permite registrar productos, controlar inventarios, manejar ventas, aplicar promociones y registrar diferentes métodos de pago. Su propósito es **reducir errores**, **optimizar el tiempo de atención al cliente** y **mejorar el control administrativo**.

---

##  Objetivos del sistema

- Registrar productos con código, nombre, precio y stock.  
- Controlar el inventario y alertar sobre productos agotados.  
- Registrar ventas y aplicar promociones o descuentos.  
- Soportar múltiples métodos de pago (efectivo, tarjeta, transferencia).  
- Gestionar sesiones individuales por usuario o turno.  
- Generar reportes de ventas e inventarios actualizados.

---

##  Arquitectura del sistema

- **Lenguaje:** Python 3.13  
- **Base de datos:** MySQL  
- **Interfaz gráfica:** Tkinter  
- **Librerías adicionales:**  
  - `mysql.connector`  
  - `tkinter.ttk`  
  - `messagebox`  
  - `datetime`  

---

##  Estructura del proyecto

```
Sistema_Punto_Venta/
│
├── database.py           # Conexión y manejo de base de datos
├── dashboard.py          # Interfaz principal del sistema
├── login.py              # Pantalla de inicio de sesión
├── ventas.py             # Módulo de registro de ventas
├── inventario.py         # Módulo de gestión de productos
├── usuarios.py           # Control de roles y usuarios
├── reportes.py           # Generación de reportes
├── /assets               # Imágenes, íconos o recursos gráficos
└── /sql                  # Script SQL de creación de tablas
```

---

##  Base de datos (MySQL)

Ejemplo del script de creación de tabla:

```sql
CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo VARCHAR(50),
    precio DECIMAL(10,2),
    stock INT,
    marca VARCHAR(50)
);
```

La base de datos incluye tablas como:
- `productos`
- `ventas`
- `clientes`
- `usuarios`
- `promociones`

---

## ⚙️ Instalación y configuración

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/tuusuario/sistema-punto-venta.git
   cd sistema-punto-venta
   ```

2. **Instala las dependencias:**
   ```bash
   pip install mysql-connector-python
   ```

3. **Crea la base de datos en MySQL:**
   ```sql
   CREATE DATABASE punto_venta;
   USE punto_venta;
   SOURCE sql/estructura.sql;
   ```

4. **Configura la conexión en `database.py`:**
   ```python
   conexion = mysql.connector.connect(
       host='localhost',
       user='root',
       password='',
       database='punto_venta'
   )
   ```

5. **Ejecuta el programa:**
   ```bash
   python dashboard.py
   ```

---

##  Metodología utilizada

- **Design Thinking:** para centrar el diseño en el usuario.  
- **Kanban:** para la gestión del trabajo en equipo.  
- **Objetivos SMART:** para definir metas medibles y alcanzables.  
- **Modelo Canvas:** para estructurar la propuesta de valor y recursos.

---

##  Beneficios del sistema

- Reducción de errores humanos en el registro de ventas.  
- Actualización automática del inventario.  
- Mayor control de ganancias y promociones.  
- Reportes que facilitan la toma de decisiones.  
- Interfaz intuitiva y moderna para los empleados.

---

##  Equipo de desarrollo

| Integrante | Rol principal |
|-------------|---------------|
| Iris Yadira Santiago | Backend  |
| Danna Michell Robles | Frontend |
| Lucía Medina | Frontend |
| Cindy Alejandra Reyes | Backend |
| Owen Asaf Benítez | Frontend |

---

##  Licencia

Este proyecto fue desarrollado con fines académicos en la **Universidad Tecnológica de Durango**.  
Su uso es libre para fines educativos y de aprendizaje.
