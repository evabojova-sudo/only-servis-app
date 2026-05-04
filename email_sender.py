import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

load_dotenv(override=True)

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SENDER = os.getenv("GMAIL_SENDER", "")
APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "")


def posli_ponuku(
    email_zakaznika: str,
    cislo_ponuky: str,
    zakaznik_meno: str,
    pdf_bytes: bytes,
    pdf_filename: str,
) -> None:
    """Odošle email zákazníkovi s PDF ponukou v prílohe."""
    msg = MIMEMultipart()
    msg["From"] = SENDER
    msg["To"] = email_zakaznika
    msg["Subject"] = f"Cenová ponuka {cislo_ponuky} – only servis s.r.o."

    body = f"""Dobrý deň, {zakaznik_meno},

v prílohe Vám zasielame cenovú ponuku č. {cislo_ponuky}.

V prípade otázok nás neváhajte kontaktovať.

S pozdravom,
Machala Roman
only servis s.r.o.
Tel: 0903 533 534
info@climaxsk.sk
"""
    msg.attach(MIMEText(body, "plain", "utf-8"))

    attachment = MIMEApplication(pdf_bytes, _subtype="pdf")
    attachment.add_header("Content-Disposition", "attachment", filename=pdf_filename)
    msg.attach(attachment)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(SENDER, APP_PASSWORD)
        smtp.sendmail(SENDER, email_zakaznika, msg.as_bytes())
