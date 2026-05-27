import base64
import os

import resend
from dotenv import load_dotenv

load_dotenv(override=True)

resend.api_key = os.getenv("RESEND_API_KEY", "")

SENDER = os.getenv("GMAIL_SENDER", "onboarding@resend.dev")

PODPIS = """\nS pozdravom,
machala roman
Tel: 0903 533 534
info@onlyservis.sk"""


def _oslovenie(meno: str) -> str:
    priezvisko = meno.strip().split()[-1] if meno.strip() else ""
    return f"pani {meno}" if priezvisko.lower().endswith("ová") else f"pán {meno}"


def posli_ponuku(
    email_zakaznika: str,
    cislo_ponuky: str,
    zakaznik_meno: str,
    pdf_bytes: bytes,
    pdf_filename: str,
    email_body: str = "",
) -> None:
    """Odošle jeden PDF ako samostatná ponuka."""
    if email_body:
        body = email_body + PODPIS
    else:
        body = (
            f"Dobrý deň {_oslovenie(zakaznik_meno)},\n\n"
            f"v prílohe Vám zasielame cenovú ponuku č. {cislo_ponuky}.\n\n"
            f"V prípade otázok nás neváhajte kontaktovať."
            f"{PODPIS}"
        )

    resend.Emails.send({
        "from": SENDER,
        "to": email_zakaznika,
        "subject": f"Cenová ponuka {cislo_ponuky} – only servis s.r.o.",
        "text": body,
        "attachments": [{
            "filename": pdf_filename,
            "content": list(pdf_bytes),
        }],
    })


def posli_zakazku(
    email_zakaznika: str,
    zakaznik_meno: str,
    polozky: list[tuple[bytes, str, dict]],
    email_body: str = "",
) -> None:
    """Odošle jeden súhrnný email so všetkými PDF v prílohe."""
    if email_body:
        body_text = email_body + PODPIS
    else:
        riadky = [
            f"Dobrý deň {_oslovenie(zakaznik_meno)},\n",
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
        body_text = "\n".join(riadky)

    attachments = [
        {"filename": pdf_filename, "content": list(pdf_bytes)}
        for pdf_bytes, pdf_filename, _ in polozky
    ]

    resend.Emails.send({
        "from": SENDER,
        "to": email_zakaznika,
        "subject": f"Cenová ponuka – {zakaznik_meno} – only servis s.r.o.",
        "text": body_text,
        "attachments": attachments,
    })
