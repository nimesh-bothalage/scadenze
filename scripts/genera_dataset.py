"""Genera scadenze/data/scadenze_2026.json con le scadenze fiscali 2026.

Fonti: scadenzario Agenzia delle Entrate + stampa di settore (luglio 2026).
Il 16 del mese slitta quando cade nel weekend: maggio -> 18, agosto -> 20
(differimento feriale ex art. 37 c.11-bis DL 223/2006).
"""

import json
from pathlib import Path

MESI = [
    "gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno",
    "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre",
]

# giorno effettivo del "16 del mese" nel 2026
GIORNO_16 = {1: 16, 2: 16, 3: 16, 4: 16, 5: 18, 6: 16, 7: 16, 8: 20, 9: 16, 10: 16, 11: 16, 12: 16}

NOTA_SLITTAMENTO = {5: "; il 16 cade di sabato", 8: "; differimento feriale"}

scadenze = []

# --- Versamenti mensili F24: IVA e ritenute -------------------------------
for mese in range(1, 13):
    mese_rif = MESI[mese - 2] if mese > 1 else "dicembre"
    anno_rif = 2026 if mese > 1 else 2025
    data = f"2026-{mese:02d}-{GIORNO_16[mese]:02d}"
    nota = NOTA_SLITTAMENTO.get(mese, "")
    scadenze.append({
        "id": f"iva-liquidazione-2026-{mese:02d}",
        "data": data,
        "titolo": "Liquidazione IVA mensile",
        "descrizione": f"Versamento IVA relativa a {mese_rif} {anno_rif} (contribuenti mensili{nota})",
        "categoria": "iva",
        "soggetti": ["partita_iva_mensile"],
        "modello": "F24",
        "ricorrenza": "mensile",
    })
    scadenze.append({
        "id": f"ritenute-2026-{mese:02d}",
        "data": data,
        "titolo": "Versamento ritenute",
        "descrizione": f"Ritenute IRPEF su redditi di lavoro dipendente e autonomo operate a {mese_rif} {anno_rif}"
        + (f" ({nota.lstrip('; ')})" if nota else ""),
        "categoria": "ritenute",
        "soggetti": ["sostituti_imposta"],
        "modello": "F24",
        "ricorrenza": "mensile",
    })

# --- IVA trimestrale -------------------------------------------------------
for trimestre, (data, rif) in {
    1: ("2026-05-18", "1° trimestre 2026, con maggiorazione dell'1% (contribuenti trimestrali; il 16 cade di sabato)"),
    2: ("2026-08-20", "2° trimestre 2026, con maggiorazione dell'1% (contribuenti trimestrali; differimento feriale)"),
    3: ("2026-11-16", "3° trimestre 2026, con maggiorazione dell'1% (contribuenti trimestrali)"),
}.items():
    scadenze.append({
        "id": f"iva-trimestrale-2026-q{trimestre}",
        "data": data,
        "titolo": f"Liquidazione IVA {trimestre}° trimestre",
        "descrizione": f"Versamento IVA relativa al {rif}",
        "categoria": "iva",
        "soggetti": ["partita_iva_trimestrale"],
        "modello": "F24",
        "ricorrenza": "trimestrale",
    })

# --- LIPE ------------------------------------------------------------------
for id_, data, rif in [
    ("lipe-2025-q4", "2026-03-02", "4° trimestre 2025 (il 28/2 cade di sabato; assorbita dalla dichiarazione IVA se presentata entro febbraio)"),
    ("lipe-2026-q1", "2026-06-01", "1° trimestre 2026 (il 31/5 cade di domenica)"),
    ("lipe-2026-q2", "2026-09-30", "2° trimestre 2026"),
    ("lipe-2026-q3", "2026-11-30", "3° trimestre 2026"),
]:
    scadenze.append({
        "id": id_,
        "data": data,
        "titolo": f"LIPE {rif.split(' (')[0]}",
        "descrizione": f"Comunicazione liquidazioni periodiche IVA relative al {rif}",
        "categoria": "iva",
        "soggetti": ["partita_iva"],
        "modello": "LIPE",
        "ricorrenza": "trimestrale",
    })

# --- Bollo fatture elettroniche -------------------------------------------
for id_, data, rif in [
    ("bollo-fe-2025-q4", "2026-03-02", "4° trimestre 2025 (il 28/2 cade di sabato)"),
    ("bollo-fe-2026-q1", "2026-06-01", "1° trimestre 2026 (il 31/5 cade di domenica; rinviabile al 30/9 se l'importo non supera 5.000 euro)"),
    ("bollo-fe-2026-q2", "2026-09-30", "2° trimestre 2026"),
    ("bollo-fe-2026-q3", "2026-11-30", "3° trimestre 2026"),
]:
    scadenze.append({
        "id": id_,
        "data": data,
        "titolo": f"Bollo fatture elettroniche {rif.split(' (')[0]}",
        "descrizione": f"Versamento imposta di bollo sulle fatture elettroniche del {rif}",
        "categoria": "bollo",
        "soggetti": ["partita_iva"],
        "modello": "F24",
        "ricorrenza": "trimestrale",
    })

# --- INPS artigiani e commercianti ----------------------------------------
for rata, (data, nota) in {
    4: ("2026-02-16", "4ª rata fissa 2025"),
    1: ("2026-05-18", "1ª rata fissa 2026 (il 16 cade di sabato)"),
    2: ("2026-08-20", "2ª rata fissa 2026 (differimento feriale al 20/8)"),
    3: ("2026-11-16", "3ª rata fissa 2026"),
}.items():
    scadenze.append({
        "id": f"inps-artigiani-{data[:7]}",
        "data": data,
        "titolo": "Contributi INPS artigiani e commercianti",
        "descrizione": f"Versamento {nota} dei contributi sul minimale di reddito",
        "categoria": "inps",
        "soggetti": ["artigiani_commercianti"],
        "modello": "F24",
        "ricorrenza": "trimestrale",
    })

# --- Scadenze una tantum ---------------------------------------------------
scadenze += [
    {
        "id": "inail-autoliquidazione-2026",
        "data": "2026-02-16",
        "titolo": "Autoliquidazione INAIL",
        "descrizione": "Versamento premio INAIL: regolazione 2025 e rata 2026 (o prima rata)",
        "categoria": "inail",
        "soggetti": ["datori_lavoro"],
        "modello": "F24",
        "ricorrenza": "annuale",
    },
    {
        "id": "iva-saldo-2025",
        "data": "2026-03-16",
        "titolo": "Saldo IVA annuale 2025",
        "descrizione": "Versamento saldo IVA risultante dalla dichiarazione annuale 2025 (rateizzabile)",
        "categoria": "iva",
        "soggetti": ["partita_iva"],
        "modello": "F24",
        "ricorrenza": "annuale",
    },
    {
        "id": "cu-2026-invio",
        "data": "2026-03-16",
        "titolo": "Certificazione Unica: invio e consegna",
        "descrizione": "Invio telematico all'Agenzia delle Entrate e consegna ai percipienti delle CU 2026 (redditi 2025)",
        "categoria": "dichiarazioni",
        "soggetti": ["sostituti_imposta"],
        "modello": "CU",
        "ricorrenza": "annuale",
    },
    {
        "id": "vidimazione-libri-sociali-2026",
        "data": "2026-03-16",
        "titolo": "Tassa vidimazione libri sociali",
        "descrizione": "Versamento tassa annuale di concessione governativa per la numerazione dei libri sociali (società di capitali)",
        "categoria": "societa",
        "soggetti": ["societa_capitali"],
        "modello": "F24",
        "ricorrenza": "annuale",
    },
    {
        "id": "cu-2026-autonomi",
        "data": "2026-03-31",
        "titolo": "Certificazione Unica lavoro autonomo",
        "descrizione": "Invio telematico delle CU 2026 contenenti solo redditi di lavoro autonomo abituale",
        "categoria": "dichiarazioni",
        "soggetti": ["sostituti_imposta"],
        "modello": "CU",
        "ricorrenza": "annuale",
    },
    {
        "id": "dichiarazione-iva-2026",
        "data": "2026-04-30",
        "titolo": "Dichiarazione IVA annuale",
        "descrizione": "Termine di presentazione della dichiarazione IVA 2026 relativa al 2025",
        "categoria": "iva",
        "soggetti": ["partita_iva"],
        "modello": "IVA 2026",
        "ricorrenza": "annuale",
    },
    {
        "id": "imposte-saldo-acconto-2026",
        "data": "2026-06-30",
        "titolo": "Saldo 2025 e 1° acconto 2026 imposte",
        "descrizione": "Versamento saldo 2025 e primo acconto 2026 di IRPEF/IRES/IRAP e contributi INPS eccedenti il minimale (termine ordinario; +0,40% entro il 30/7)",
        "categoria": "imposte",
        "soggetti": ["persone_fisiche", "societa"],
        "modello": "F24",
        "ricorrenza": "annuale",
    },
    {
        "id": "imu-acconto-2026",
        "data": "2026-06-16",
        "titolo": "IMU: acconto",
        "descrizione": "Versamento prima rata IMU 2026",
        "categoria": "imu",
        "soggetti": ["proprietari_immobili"],
        "modello": "F24",
        "ricorrenza": "annuale",
    },
    {
        "id": "imposte-saldo-acconto-2026-isa",
        "data": "2026-07-20",
        "titolo": "Saldo e 1° acconto imposte (soggetti ISA e forfettari)",
        "descrizione": "Versamento saldo 2025 e primo acconto 2026 senza maggiorazione per soggetti ISA, forfettari e minimi (proroga D.L. 89/2026; +0,80% entro il 20/8)",
        "categoria": "imposte",
        "soggetti": ["soggetti_isa", "forfettari"],
        "modello": "F24",
        "ricorrenza": "annuale",
    },
    {
        "id": "modello-730-2026",
        "data": "2026-09-30",
        "titolo": "Modello 730/2026: presentazione",
        "descrizione": "Termine di presentazione del modello 730/2026 (redditi 2025)",
        "categoria": "dichiarazioni",
        "soggetti": ["persone_fisiche"],
        "modello": "730",
        "ricorrenza": "annuale",
    },
    {
        "id": "redditi-2026-presentazione",
        "data": "2026-11-02",
        "titolo": "Modello Redditi e IRAP 2026: presentazione",
        "descrizione": "Termine di presentazione telematica dei modelli Redditi PF/SP/SC e IRAP 2026 (il 31/10 cade di sabato)",
        "categoria": "dichiarazioni",
        "soggetti": ["persone_fisiche", "societa"],
        "modello": "Redditi",
        "ricorrenza": "annuale",
    },
    {
        "id": "modello-770-2026",
        "data": "2026-11-02",
        "titolo": "Modello 770/2026: presentazione",
        "descrizione": "Termine di presentazione della dichiarazione dei sostituti d'imposta 770/2026 (il 31/10 cade di sabato)",
        "categoria": "dichiarazioni",
        "soggetti": ["sostituti_imposta"],
        "modello": "770",
        "ricorrenza": "annuale",
    },
    {
        "id": "imposte-secondo-acconto-2026",
        "data": "2026-11-30",
        "titolo": "2° acconto imposte 2026",
        "descrizione": "Versamento secondo o unico acconto 2026 di IRPEF/IRES/IRAP e contributi INPS eccedenti il minimale",
        "categoria": "imposte",
        "soggetti": ["persone_fisiche", "societa"],
        "modello": "F24",
        "ricorrenza": "annuale",
    },
    {
        "id": "imu-saldo-2026",
        "data": "2026-12-16",
        "titolo": "IMU: saldo",
        "descrizione": "Versamento seconda rata IMU 2026 a conguaglio",
        "categoria": "imu",
        "soggetti": ["proprietari_immobili"],
        "modello": "F24",
        "ricorrenza": "annuale",
    },
    {
        "id": "acconto-iva-2026",
        "data": "2026-12-28",
        "titolo": "Acconto IVA 2026",
        "descrizione": "Versamento acconto IVA per il 2026, metodo storico, previsionale o analitico (il 27/12 cade di domenica)",
        "categoria": "iva",
        "soggetti": ["partita_iva"],
        "modello": "F24",
        "ricorrenza": "annuale",
    },
]

scadenze.sort(key=lambda s: (s["data"], s["id"]))

ids = [s["id"] for s in scadenze]
assert len(ids) == len(set(ids)), "id duplicati"

dest = Path(__file__).resolve().parent.parent / "scadenze" / "data" / "scadenze_2026.json"
dest.write_text(json.dumps(scadenze, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Scritte {len(scadenze)} scadenze in {dest}")
