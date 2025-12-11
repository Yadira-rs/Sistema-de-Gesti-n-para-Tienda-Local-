from database.db import crear_conexion
import smtplib
from email.mime.text import MIMEText

class AuthController:

    def login(self, email, password):
        """
        Autentica a un usuario.
        NOTA: Las contraseñas están almacenadas en texto plano en la base de datos.
        """
        try:
            conn = crear_conexion()
            if conn is None:
                return None
                
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE email=%s AND activo=1", (email,))
            user = cursor.fetchone()
            
            conn.close()

            if user and 'contraseña' in user:
                # Comparación directa ya que las contraseñas están en texto plano
                if user['contraseña'] == password:
                    return user
            
            return None

        except Exception as e:
            print(f"Error en AuthController.login: {e}")
            return None

    def send_recovery_email(self, email):
        """
        Envía un correo de recuperación de contraseña.
        NOTA: Esta función parece estar incompleta/no funcional en el código original.
              No se recomienda su uso sin una configuración adecuada de SMTP
              y una revisión de seguridad.
        """
        try:
            with crear_conexion() as conn:
                if conn is None or not conn.is_connected():
                    return False
                
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute("SELECT * FROM usuarios WHERE email=%s", (email,))
                    user = cursor.fetchone()

            if not user:
                return False
            
            # La siguiente parte es un EJEMPLO y requiere configuración real
            # No es seguro enviar contraseñas en texto plano por correo.
            password = "LA CONTRASEÑA NO DEBERÍA ENVIARSE ASÍ" # user['contraseña'] es un hash

            message = MIMEText(f"Hola {user['nombre_completo']},\n\nSe solicitó una recuperación de contraseña. "
                               f"Tu contraseña es: {password}\n\n"
                               f"Por favor, cámbiala después de iniciar sesión.")
            message['Subject'] = "Recuperación de contraseña - Boutique Rosa Janet"
            message['From'] = "noreply@boutique.com" # Debe ser un correo real
            message['To'] = email

            # Requiere un servidor SMTP configurado
            # server = smtplib.SMTP("smtp.gmail.com", 587)
            # server.starttls()
            # server.login("tu_correo@gmail.com", "TU_APP_PASSWORD")
            # server.sendmail("tu_correo@gmail.com", email, message.as_string())
            # server.quit()

            print("Correo de recuperación enviado (simulado).")
            return True

        except Exception as e:
            print(f"Error en AuthController.send_recovery_email: {e}")
            return False

# Autenticación con contraseñas en texto plano