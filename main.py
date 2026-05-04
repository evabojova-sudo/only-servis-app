import base64
import json
import os
import re

import anthropic
from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles

from database import init_db, uloz_ponuku, oznac_email_odoslany
from email_sender import posli_ponuku
from pdf_generator import generuj_pdf, zisti_produkt

load_dotenv(override=True)

app = FastAPI(title="OnlyServis API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# Inicializácia DB pri štarte (ak DATABASE_URL je nastavené)
if os.getenv("DATABASE_URL"):
    try:
        init_db()
    except Exception as e:
        print(f"[DB] init_db zlyhal: {e}")

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

EXTRACTION_PROMPT = """Si asistent na extrakciu dát z PDF cenových ponúk systému Climax (tienacia technika).

Prečítaj tento PDF vizuálne a extrahuj VŠETKY nasledujúce polia do JSON formátu.
Ak pole v PDF neexistuje, vráť null.

Polia ktoré musíš extrahovať:
- cislo_ponuky: číslo ponuky (napr. "21042026_Dujnicova_Z90io")
- zakaznik_meno: priezvisko alebo meno zákazníka
- zakaznik_mesto: mesto zákazníka
- datum_ponuky: dátum ponuky vo formáte DD.MM.YYYY
- typ_produktu: kód produktu (napr. "Z-90-NOVAL")
- pocet_ks: počet kusov (integer)
- rozmer_sirka_cm: šírka v cm (number alebo null)
- rozmer_vyska_cm: výška v cm (number alebo null)
- cena_bez_dph: cena bez DPH (number)
- zlava_percent: zľava v percentách (number alebo null)
- zlava_suma: suma zľavy (number alebo null)
- cena_po_zlave: cena po zľave pred DPH (number alebo null)
- dph_percent: sadzba DPH v percentách (number)
- dph_suma: suma DPH (number)
- cena_s_dph: finálna cena s DPH (number)
- priplatky: JSON array objektov {nazov: string, suma: number} pre všetky príplatky (Montáž, Doprava, atď.)

Vráť LEN čistý JSON bez akéhokoľvek ďalšieho textu alebo markdown formátovania."""


@app.get("/")
def root():
    return {"status": "ok", "app": "OnlyServis API", "faza": 2}


@app.post("/extract-pdf")
async def extract_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Súbor musí byť PDF")

    pdf_bytes = await file.read()
    if len(pdf_bytes) == 0:
        raise HTTPException(status_code=400, detail="PDF súbor je prázdny")

    pdf_b64 = base64.standard_b64encode(pdf_bytes).decode("utf-8")

    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "document",
                        "source": {
                            "type": "base64",
                            "media_type": "application/pdf",
                            "data": pdf_b64,
                        },
                    },
                    {
                        "type": "text",
                        "text": EXTRACTION_PROMPT,
                    },
                ],
            }
        ],
    )

    response_text = message.content[0].text.strip()
    response_text = re.sub(r"^```(?:json)?\s*", "", response_text)
    response_text = re.sub(r"\s*```$", "", response_text)

    return json.loads(response_text)


@app.post("/generate-pdf")
async def generate_pdf(data: dict):
    """Prijme JSON s extrahovanými dátami, vráti PDF ponuku Only Servis."""
    required = ["cislo_ponuky", "zakaznik_meno", "cena_s_dph"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        raise HTTPException(status_code=400, detail=f"Chýbajú polia: {missing}")

    pdf_bytes = generuj_pdf(data)

    cislo = data.get("cislo_ponuky", "ponuka").replace("/", "_")
    filename = f"OnlyServis_{cislo}.pdf"

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@app.post("/process")
async def process(
    file: UploadFile = File(...),
    email_zakaznika: str = Form(default=""),
):
    """
    Kompletný workflow: PDF → extrakcia → generovanie → uloženie do DB.
    Vráti JSON s extrahovanými dátami, db_ids a PDF ako base64.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Súbor musí byť PDF")

    pdf_bytes = await file.read()
    pdf_b64 = base64.standard_b64encode(pdf_bytes).decode("utf-8")

    # 1. Extrakcia cez Claude API
    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": [
                {"type": "document", "source": {"type": "base64", "media_type": "application/pdf", "data": pdf_b64}},
                {"type": "text", "text": EXTRACTION_PROMPT},
            ],
        }],
    )
    response_text = message.content[0].text.strip()
    response_text = re.sub(r"^```(?:json)?\s*", "", response_text)
    response_text = re.sub(r"\s*```$", "", response_text)
    extrahovane = json.loads(response_text)

    # Doplň slovenský názov produktu
    slovensky_nazov, _, _ = zisti_produkt(extrahovane.get("typ_produktu", ""))
    extrahovane["slovensky_nazov"] = slovensky_nazov

    # 2. Generovanie PDF ponuky Only Servis
    output_pdf = generuj_pdf(extrahovane)
    output_pdf_b64 = base64.standard_b64encode(output_pdf).decode("utf-8")

    # 3. Uloženie do DB (ak je DATABASE_URL nastavené)
    db_ids = {}
    if os.getenv("DATABASE_URL"):
        try:
            db_ids = uloz_ponuku(extrahovane, email_zakaznika or None)
        except Exception as e:
            print(f"[DB] Chyba pri ukladaní: {e}")

    cislo = extrahovane.get("cislo_ponuky", "ponuka").replace("/", "_")
    pdf_filename = f"OnlyServis_{cislo}.pdf"

    # 4. Odoslanie emailu (ak je zadaná adresa)
    email_odoslany = False
    if email_zakaznika and os.getenv("GMAIL_SENDER"):
        try:
            posli_ponuku(
                email_zakaznika=email_zakaznika,
                cislo_ponuky=extrahovane.get("cislo_ponuky", ""),
                zakaznik_meno=extrahovane.get("zakaznik_meno", ""),
                pdf_bytes=output_pdf,
                pdf_filename=pdf_filename,
            )
            email_odoslany = True
            if db_ids.get("ponuka_id"):
                oznac_email_odoslany(db_ids["ponuka_id"])
        except Exception as e:
            print(f"[EMAIL] Chyba pri odoslaní: {e}")

    return {
        "extrahovane": extrahovane,
        "pdf_filename": pdf_filename,
        "pdf_base64": output_pdf_b64,
        "db": db_ids,
        "email_odoslany": email_odoslany,
    }
