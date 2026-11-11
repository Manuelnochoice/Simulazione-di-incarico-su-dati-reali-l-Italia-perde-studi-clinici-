"""
03_salto_2023.py

Indaga il salto del 2023 negli studi OSSERVAZIONALI con sede in Italia
(462 nel 2022 -> 970 nel 2023, mentre gli altri paesi restano fermi).

Scarica l'elenco degli studi osservazionali italiani registrati dal 2021 al 2025
e mostra, anno per anno, quali sponsor li hanno registrati.
Domanda: il salto e' distribuito su molti enti (cambiamento reale) oppure concentrato
in pochi (registrazione in blocco o cambio di regola)?

OUTPUT
- output/italia_osservazionali_dettaglio.csv (un record per studio)
- riepilogo a schermo: sponsor principali per anno, categoria di sponsor, concentrazione

NOTA: non provato sull'API reale. Se la struttura del JSON differisce, la funzione
estrai_righe() e' l'unico punto da adattare.
"""

import time
from datetime import date
from pathlib import Path

import pandas as pd
import requests

URL = "https://clinicaltrials.gov/api/v2/studies"
ANNI = range(2021, 2026)
PAUSA = 0.5
CARTELLA_OUTPUT = Path(__file__).resolve().parent.parent / "output"


def estrai_righe(pagina):
    """Trasforma una pagina JSON dell'API in una lista di dizionari semplici."""
    righe = []
    for studio in pagina.get("studies", []):
        protocollo = studio.get("protocolSection", {})
        identificazione = protocollo.get("identificationModule", {})
        stato = protocollo.get("statusModule", {})
        sponsor = protocollo.get("sponsorCollaboratorsModule", {}).get("leadSponsor", {})
        righe.append(
            {
                "nct_id": identificazione.get("nctId"),
                "titolo": identificazione.get("briefTitle"),
                "data_registrazione": stato.get("studyFirstSubmitDate"),
                "sponsor": sponsor.get("name"),
                "categoria_sponsor": sponsor.get("class"),
            }
        )
    return righe


def scarica_anno(anno):
    """Scarica tutti gli studi osservazionali italiani registrati in un anno (con paginazione)."""
    filtro = (
        "AREA[StudyType]OBSERVATIONAL AND AREA[LocationCountry]Italy AND "
        f"AREA[StudyFirstSubmitDate]RANGE[{anno}-01-01,{anno}-12-31]"
    )
    params = {
        "filter.advanced": filtro,
        "pageSize": 1000,
        "countTotal": "true",
        "fields": "NCTId|BriefTitle|StudyFirstSubmitDate|LeadSponsorName|LeadSponsorClass",
    }
    righe = []
    totale_atteso = None
    while True:
        r = requests.get(URL, params=params, timeout=60)
        r.raise_for_status()
        pagina = r.json()
        if totale_atteso is None:
            totale_atteso = pagina.get("totalCount")
        righe.extend(estrai_righe(pagina))
        token = pagina.get("nextPageToken")
        if not token:
            break
        params["pageToken"] = token
        time.sleep(PAUSA)
    # Verifica di completezza: gli studi scaricati devono coincidere con il conteggio dell'API
    if totale_atteso is not None and totale_atteso != len(righe):
        print(f"  ATTENZIONE {anno}: attesi {totale_atteso}, scaricati {len(righe)}")
    for riga in righe:
        riga["anno"] = anno
    return righe


def main():
    CARTELLA_OUTPUT.mkdir(exist_ok=True)
    tutte = []
    for anno in ANNI:
        righe = scarica_anno(anno)
        print(f"{anno}: {len(righe)} studi")
        tutte.extend(righe)
        time.sleep(PAUSA)

    df = pd.DataFrame(tutte)
    df["data_estrazione"] = date.today().isoformat()
    df.to_csv(CARTELLA_OUTPUT / "italia_osservazionali_dettaglio.csv", index=False, encoding="utf-8")

    print("\n=== Studi per anno e categoria di sponsor ===")
    print(df.pivot_table(index="anno", columns="categoria_sponsor", values="nct_id", aggfunc="count", fill_value=0))

    print("\n=== Concentrazione: quota dei primi 5 sponsor sul totale dell'anno ===")
    for anno, gruppo in df.groupby("anno"):
        conteggio = gruppo["sponsor"].value_counts()
        quota_top5 = conteggio.head(5).sum() / len(gruppo) * 100
        print(f"{anno}: {len(gruppo)} studi, {conteggio.size} sponsor diversi, primi 5 = {quota_top5:.0f}%")

    print("\n=== Primi 10 sponsor, 2022 contro 2023 ===")
    for anno in (2022, 2023):
        print(f"\n{anno}")
        print(df[df["anno"] == anno]["sponsor"].value_counts().head(10).to_string())

    print("\nSalvato: output/italia_osservazionali_dettaglio.csv")


if __name__ == "__main__":
    main()
