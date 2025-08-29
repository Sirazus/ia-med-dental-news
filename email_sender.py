# email_sender.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL_USER, EMAIL_APP_PASSWORD, EMAIL_TO

def send_email(summary_text):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "🤖 IA en Medicina y Odontología - Resumen Semanal"
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_TO

    html = f"""
    <html>
      <body>
        <h1>📰 Resumen semanal: IA en Salud</h1>
        <p><strong>Noticias destacadas:</strong></p>
        <pre style="background:#f4f4f4; padding:15px; border-radius:5px; font-family:monospace; font-size:14px;">
        {summary_text}
        </pre>
        <br>
        <h3>🎙️ Tu turno: genera el podcast</h3>
        <p>Copia el texto anterior y pásalo a <a href="https://notebooklm.google.com">Notebook LM</a> para generar el audio.</p>
        <p>Después, sube el archivo MP3 a la carpeta <code>output/</code> del repositorio.</p>
      </body>
    </html>
    """

    part = MIMEText(html, "html")
    msg.attach(part)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_APP_PASSWORD)
        server.sendmail(EMAIL_USER, EMAIL_TO, msg.as_string())
        server.close()
        print("✅ Email enviado")
    except Exception as e:
        print("❌ Error al enviar email:", str(e))
