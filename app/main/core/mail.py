import smtplib
import logging
from datetime import datetime, timedelta
from email import encoders
from email.mime.base import MIMEBase
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Template
from app.main.core.config import Config

def send_account_creation_email(email_to: str, first_name: str, last_name: str, password: str) -> None:
    try:
        # Chargement du template HTML
        template_path = Path(Config.EMAIL_TEMPLATES_DIR) / "account_creation.html"
        html_content = Template(template_path.read_text(encoding="utf-8")).render(
            first_name=first_name,
            last_name=last_name,
            password=password,
            project_name=Config.PROJECT_NAME
        )

        # Création de l'email
        msg = MIMEMultipart()
        msg["From"] = f"{Config.EMAILS_FROM_NAME} <{Config.EMAILS_FROM_EMAIL}>"
        msg["To"] = email_to
        msg["Subject"] = f"{Config.EMAILS_FROM_NAME} | Compte créé"
        msg.attach(MIMEText(html_content, "html"))

        # Connexion et envoi
        with smtplib.SMTP(Config.SMTP_HOST, Config.SMTP_PORT) as server:
            if Config.SMTP_TLS:
                server.starttls()
            server.login(Config.SMTP_USER, Config.SMTP_PASSWORD)
            server.send_message(msg)

        logging.info(f"✅ Email envoyé à {email_to}")

    except Exception as e:
        logging.error(f"❌ Erreur lors de l'envoi de l'email : {e}")

def send_reset_password_option2_email(email_to: str, name: str,  otp: str):
    try:
        # Chargement du template HTML
        template_path = Path(Config.EMAIL_TEMPLATES_DIR) / "reset_password_option2.html"
        html_content = Template(template_path.read_text(encoding="utf-8")).render(
            name=name,
            otp=otp,
            project_name=Config.PROJECT_NAME
        )

        # Création de l'email
        msg = MIMEMultipart()
        msg["From"] = f"{Config.EMAILS_FROM_NAME} <{Config.EMAILS_FROM_EMAIL}>"
        msg["To"] = email_to
        msg["Subject"] = f"{Config.EMAILS_FROM_NAME} | Réinitialisation du mot de passe"
        msg.attach(MIMEText(html_content, "html"))

        # Connexion et envoi
        with smtplib.SMTP(Config.SMTP_HOST, Config.SMTP_PORT) as server:
            if Config.SMTP_TLS:
                server.starttls()
            server.login(Config.SMTP_USER, Config.SMTP_PASSWORD)
            server.send_message(msg)

        logging.info(f"✅ Email envoyé à {email_to}")

    except Exception as e:
        logging.error(f"❌ Erreur lors de l'envoi de l'email : {e}")


def send_start_reset_password(email_to: str, name: str, code: str) -> None:
    try:
        # Charger le template HTML
        template_path = Path(Config.EMAIL_TEMPLATES_DIR) / "start_reset_password.html"
        html_content = Template(template_path.read_text(encoding="utf-8")).render(
            name=name,
            code=code,
            project_name=Config.PROJECT_NAME
        )

        # Créer l'email
        msg = MIMEMultipart()
        msg["From"] = f"{Config.EMAILS_FROM_NAME} <{Config.EMAILS_FROM_EMAIL}>"
        msg["To"] = email_to
        msg["Subject"] = f"{Config.EMAILS_FROM_NAME} | Réinitialisation du mot de passe"
        msg.attach(MIMEText(html_content, "html"))

        # Connexion et envoi
        with smtplib.SMTP(Config.SMTP_HOST, Config.SMTP_PORT) as server:
            if Config.SMTP_TLS:
                server.starttls()
            server.login(Config.SMTP_USER, Config.SMTP_PASSWORD)
            server.send_message(msg)

        logging.info(f"✅ Email envoyé à {email_to}")

    except Exception as e:
        logging.error(f"❌ Erreur lors de l'envoi de l'email : {e}")



def send_account_confirmation_email():
    return None




def send_code_validation(email_to: str, code: str,expirat_at:datetime,full_name:str) -> None:
    try:
        template_path = Path(Config.EMAIL_TEMPLATES_DIR) / "code_validation.html"
        html_content = Template(template_path.read_text(encoding="utf-8")).render(
            email_to=email_to,
            code=code,
            expirat_at=expirat_at.strftime("%d/%m/%Y à %H:%M"),
            project_name=Config.PROJECT_NAME,
            full_name = full_name
        )
        msg = MIMEMultipart()
        msg["From"] = f"{Config.EMAILS_FROM_NAME} <{Config.EMAILS_FROM_EMAIL}>"
        msg["To"] = email_to
        msg["Subject"] = f"{Config.EMAILS_FROM_NAME} | Code de validation de votre compte"
        msg.attach(MIMEText(html_content, "html"))

        # Connexion et envoi
        with smtplib.SMTP(Config.SMTP_HOST, Config.SMTP_PORT) as server:
            if Config.SMTP_TLS:
                server.starttls()
            server.login(Config.SMTP_USER, Config.SMTP_PASSWORD)
            server.send_message(msg)

        logging.info(f"✅ Email envoyé à {email_to}")

    except Exception as e:
        logging.error(f"❌ Erreur lors de l'envoi de l'email : {e}")





def send_owner_message_for_new_reservation(email_to: str, full_name:str,message:str,code) -> None:
    try:
        template_path = Path(Config.EMAIL_TEMPLATES_DIR) / "new_reservation.html"
        html_content = Template(template_path.read_text(encoding="utf-8")).render(
            email_to=email_to,
            code=code,
            full_name=full_name,
            message=message,
            project_name=Config.PROJECT_NAME,
        )
        msg = MIMEMultipart()
        msg["From"] = f"{Config.EMAILS_FROM_NAME} <{Config.EMAILS_FROM_EMAIL}>"
        msg["To"] = email_to
        msg["Subject"] = f"{Config.EMAILS_FROM_NAME} | Nouvelle reservation"
        msg.attach(MIMEText(html_content, "html"))

        with smtplib.SMTP(Config.SMTP_HOST, Config.SMTP_PORT) as server:
            if Config.SMTP_TLS:
                server.starttls()
            server.login(Config.SMTP_USER, Config.SMTP_PASSWORD)
            server.send_message(msg)

        logging.info(f"✅ Email envoyé à {email_to}")

    except Exception as e:
        logging.error(f"❌ Erreur lors de l'envoi de l'email : {e}")

