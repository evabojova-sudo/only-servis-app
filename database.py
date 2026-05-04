import os
import uuid
from datetime import datetime, date

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv(override=True)

psycopg2.extras.register_uuid()


def get_conn():
    return psycopg2.connect(os.environ["DATABASE_URL"])


def init_db():
    """Vytvorí tabuľky ak neexistujú."""
    sql = """
    CREATE TABLE IF NOT EXISTS zakaznici (
        id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        meno        TEXT NOT NULL,
        email       TEXT,
        telefon     TEXT,
        adresa      TEXT,
        mesto       TEXT,
        vytvoreny   TIMESTAMP NOT NULL DEFAULT NOW()
    );

    CREATE TABLE IF NOT EXISTS ponuky (
        id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        zakaznik_id             UUID REFERENCES zakaznici(id),
        cislo_ponuky            TEXT NOT NULL,
        datum_ponuky            DATE,
        celkova_suma_bez_dph    DECIMAL(10,2),
        celkova_suma_s_dph      DECIMAL(10,2),
        email_odoslany          BOOLEAN NOT NULL DEFAULT FALSE,
        email_odoslany_datum    TIMESTAMP,
        vytvorena               TIMESTAMP NOT NULL DEFAULT NOW()
    );

    CREATE TABLE IF NOT EXISTS polozky_ponuky (
        id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        ponuka_id           UUID REFERENCES ponuky(id) ON DELETE CASCADE,
        typ_produktu        TEXT,
        slovensky_nazov     TEXT,
        pocet_ks            INTEGER,
        rozmer_sirka_cm     DECIMAL(8,2),
        rozmer_vyska_cm     DECIMAL(8,2),
        cena_bez_dph        DECIMAL(10,2),
        zlava_percent       DECIMAL(5,2),
        cena_s_dph          DECIMAL(10,2),
        priplatky_json      JSONB
    );
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()


def uloz_ponuku(extrahovane: dict, email_zakaznika: str | None = None) -> dict:
    """
    Uloží zákazníka, ponuku a položku do DB.
    Vráti dict s id záznamu ponuky.
    """
    meno = extrahovane.get("zakaznik_meno") or ""
    mesto = extrahovane.get("zakaznik_mesto") or ""

    # Parsuj dátum ponuky
    datum_str = extrahovane.get("datum_ponuky") or ""
    datum = None
    try:
        datum = datetime.strptime(datum_str, "%d.%m.%Y").date()
    except ValueError:
        pass

    priplatky = extrahovane.get("priplatky") or []
    priplatky_suma = sum(p.get("suma", 0) for p in priplatky)
    cena_bez_dph = (extrahovane.get("cena_po_zlave") or extrahovane.get("cena_bez_dph") or 0)
    cena_s_dph = extrahovane.get("cena_s_dph") or 0

    with get_conn() as conn:
        with conn.cursor() as cur:
            # 1. Zákazník — hľadaj podľa mena+mesta, alebo vytvor nového
            cur.execute(
                "SELECT id FROM zakaznici WHERE meno = %s AND mesto = %s LIMIT 1",
                (meno, mesto),
            )
            row = cur.fetchone()
            if row:
                zakaznik_id = row[0]
            else:
                zakaznik_id = uuid.uuid4()
                cur.execute(
                    """INSERT INTO zakaznici (id, meno, email, mesto)
                       VALUES (%s, %s, %s, %s)""",
                    (zakaznik_id, meno, email_zakaznika, mesto),
                )

            # 2. Ponuka
            ponuka_id = uuid.uuid4()
            cur.execute(
                """INSERT INTO ponuky
                   (id, zakaznik_id, cislo_ponuky, datum_ponuky,
                    celkova_suma_bez_dph, celkova_suma_s_dph)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (
                    ponuka_id,
                    zakaznik_id,
                    extrahovane.get("cislo_ponuky") or "",
                    datum,
                    float(cena_bez_dph),
                    float(cena_s_dph),
                ),
            )

            # 3. Položka ponuky
            cur.execute(
                """INSERT INTO polozky_ponuky
                   (id, ponuka_id, typ_produktu, slovensky_nazov,
                    pocet_ks, rozmer_sirka_cm, rozmer_vyska_cm,
                    cena_bez_dph, zlava_percent, cena_s_dph, priplatky_json)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                    uuid.uuid4(),
                    ponuka_id,
                    extrahovane.get("typ_produktu"),
                    extrahovane.get("slovensky_nazov"),
                    extrahovane.get("pocet_ks"),
                    extrahovane.get("rozmer_sirka_cm"),
                    extrahovane.get("rozmer_vyska_cm"),
                    extrahovane.get("cena_bez_dph"),
                    extrahovane.get("zlava_percent"),
                    float(cena_s_dph),
                    psycopg2.extras.Json(priplatky),
                ),
            )

        conn.commit()

    return {"ponuka_id": str(ponuka_id), "zakaznik_id": str(zakaznik_id)}


def oznac_email_odoslany(ponuka_id: str) -> None:
    """Označí ponuku ako odoslanú emailom."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """UPDATE ponuky SET email_odoslany = TRUE, email_odoslany_datum = NOW()
                   WHERE id = %s""",
                (ponuka_id,),
            )
        conn.commit()
