from database.db import db
from twilio.rest import Client
import smtplib
from email.mime.text import MIMEText

class AuthController:

    def login(self, email, password):
        sql = "SELECT * FROM usuarios WHERE email=%s AND password=%s"
        result = db.query(sql, (email, password))
        return result[0] if result else None

    def send_recovery_email(self, email):
        sql = "SELECT * FROM usuarios WHERE email=%s"
        result = db.query(sql, (email,))

        if not result:
            return False
        
        user = result[0]

        message = MIMEText(f"Hola {user['nombre']},\nTu contraseña es: {user['password']}")
        message['Subject'] = "Recuperación de contraseña - Boutique Rosa Janet"
        message['From'] = "noreply@boutique.com"
        message['To'] = email

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("tu_correo@gmail.com", "TU_APP_PASSWORD")
        server.sendmail("tu_correo@gmail.com", email, message.as_string())
        server.quit()

        return True
