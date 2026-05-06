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

PODPIS = """\nS pozdravom,
Machala Roman
only servis s.r.o.
Tel: 0903 533 534
info@climaxsk.sk"""


def _odosli(msg: MIMEMultipart, email_zakaznika: str) -> None:
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(SENDER, APP_PASSWORD)
        smtp.sendmail(SENDER, email_zakaznika, msg.as_bytes())


def posli_ponuku(
    email_zakaznika: str,
    cislo_ponuky: str,
    zakaznik_meno: str,
    pdf_bytes: bytes,
    pdf_filename: str,
) -> None:
    """Odošle jeden PDF ako samostatná ponuka."""
    msg = MIMEMultipart()
    msg["From"] = SENDER
    msg["To"] = email_zakaznika
    msg["Subject"] = f"Cenová ponuka {cislo_ponuky} – only servis s.r.o."

    body = (
        f"Dobrý deň, {zakaznik_meno},\n\n"
        f"v prílohe Vám zasielame cenovú ponuku č. {cislo_ponuky}.\n\n"
        f"V prípade otázok nás neváhajte kontaktovať."
        f"{PODPIS}"
    )
    msg.attach(MIMEText(body, "plain", "utf-8"))

    att = MIMEApplication(pdf_bytes, _subtype="pdf")
    att.add_header("Content-Disposition", "attachment", filename=pdf_filename)
    msg.attach(att)

    _odosli(msg, email_zakaznika)


def posli_zakazku(
    email_zakaznika: str,
    zakaznik_meno: str,
    polozky: list[tuple[bytes, str, dict]],
) -> None:
    """Odošle jeden súhrnný email so všetkými PDF v prílohe.

    polozky: zoznam (pdf_bytes, pdf_filename, data_dict) pre každý produkt.
    """
    msg = MIMEMultipart()
    msg["From"] = SENDER
    msg["To"] = email_zakaznika
    msg["Subject"] = f"Cenová ponuka – {zakaznik_meno} – only servis s.r.o."

    riadky = [
        f"Dobrý deň, {zakaznik_meno},\n",
        "v prílohe Vám zasielame cenovú ponuku pre nasledujúce produkty:\n",
    ]
    celkom = 0.0
    for _, _, d in polozky:
        nazov = d.get("slovensky_nazov") or d.get("typ_produktu") or "–"
        pocet = d.get("pocet_ks") or 1
        cena  = float(d.get("cena_s_dph") or 0)
        celkom += cena
        riadky.append(f"  • {nazov} ({pocet} ks): {cena:,.2f} €".replace(",", " "))

    riadky.append(f"\nCelková cena s DPH: {celkom:,.2f} €".replace(",", " "))
    riadky.append("\nV prípade otázok nás neváhajte kontaktovať.")
    riadky.append(PODPIS)

    msg.attach(MIMEText("\n".join(riadky), "plain", "utf-8"))

    for pdf_bytes, pdf_filename, _ in polozky:
        att = MIMEApplication(pdf_bytes, _subtype="pdf")
        att.add_header("Content-Disposition", "attachment", filename=pdf_filename)
        msg.attach(att)

    _odosli(msg, email_zakaznika)
