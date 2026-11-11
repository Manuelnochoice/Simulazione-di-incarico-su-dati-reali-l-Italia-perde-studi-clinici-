"""
01_conteggi_paesi.py

Conta, tramite l'API v2 di ClinicalTrials.gov, quanti studi sono stati registrati
per paese, anno di registrazione e tipo di studio.

DEFINIZIONI (da tenere allineate con decisioni.md)
- Studio: sia interventistico sia osservazionale (le due serie restano separate nel CSV).
- Anno: anno di PRIMA REGISTRAZIONE dello studio (campo StudyFirstSubmitDate).
- Periodo: 2016-2025, cioe' gli ultimi 10 anni completi.
- Paese: studio con ALMENO UNA SEDE nel paese (campo LocationCountry).
  Uno studio multicentrico viene quindi contato in ogni paese in cui ha sedi:
  le serie dei paesi NON vanno sommate tra loro.
- "Mondo": tutti gli studi registrati nell'anno, senza filtro di paese. Serve come
  termine di confronto: se tutti i paesi calano, il problema e' del registro, non dell'Italia.

OUTPUT
- output/conteggi_paesi_anno.csv, con la data di estrazione (l'API e' "viva": i numeri
  cambiano nel tempo, quindi la data va sempre citata).

NOTA: questo script non e' stato provato sull'API reale. Il controllo iniziale serve
proprio a verificare che la sintassi dei filtri funzioni.
"""

import time
from datetime import date
from pathlib import Path

import pandas as pd
import requests

URL = "https://clinicaltrials.gov/api/v2/studies"
PAESI = {"Italia": "Italy", "Spagna": "Spain", "Francia": "France", "Germania": "Germany"}
ANNI = range(2016, 2026)
TIPI = ["INTERVENTIONAL", "OBSERVATIONAL"]
PAUSA = 0.3  # secondi tra una richiesta e l'altra, per non sovraccaricare il servizio

CARTELLA_OUTPUT = Path(__file__).resolve().parent.parent / "output"


def chiedi_conteggio(params):
    """Esegue una richiesta e restituisce totalCount. Riprova 3 volte in caso di errore."""
    params = {**params, "countTotal": "true", "pageSize": 1, "fields": "NCTId"}
    for tentativo in range(1, 4):
        try:
            r = requests.get(URL, params=params, timeout=30)
            if r.status_code == 200:
                return r.json()["totalCount"]
            print(f"  Codice {r.status_code} (tentativo {tentativo}): {r.text[:200]}")
        except requests.RequestException as errore:
            print(f"  Errore di rete (tentativo {tentativo}): {errore}")
        time.sleep(2 * tentativo)
    raise RuntimeError(f"Richiesta fallita dopo 3 tentativi: {params}")


def conta_studi(tipo, anno, paese_api=None):
    """Numero di studi di un certo tipo, registrati in un certo anno, con sede in un paese."""
    filtri = [
        f"AREA[StudyType]{tipo}",
        f"AREA[StudyFirstSubmitDate]RANGE[{anno}-01-01,{anno}-12-31]",
    ]
    if paese_api:
        filtri.append(f"AREA[LocationCountry]{paese_api}")
    return chiedi_conteggio({"filter.advanced": " AND ".join(filtri)})


def controllo_iniziale():
    """Confronta due modi diversi di filtrare l'Italia: devono dare (quasi) lo stesso numero."""
    print("Controllo iniziale: Italia, studi interventistici registrati nel 2020")
    con_campo_paese = conta_studi("INTERVENTIONAL", 2020, "Italy")
    time.sleep(PAUSA)
    con_ricerca_libera = chiedi_conteggio(
        {
            "query.locn": "Italy",
            "filter.advanced": "AREA[StudyType]INTERVENTIONAL AND "
            "AREA[StudyFirstSubmitDate]RANGE[2020-01-01,2020-12-31]",
        }
    )
    print(f"  Con il campo LocationCountry: {con_campo_paese}")
    print(f"  Con la ricerca libera query.locn: {con_ricerca_libera}")
    if con_campo_paese == 0:
        raise RuntimeError("Conteggio a zero: la sintassi del filtro per paese non funziona.")
    differenza = abs(con_campo_paese - con_ricerca_libera) / max(con_campo_paese, 1)
    if differenza > 0.10:
        print("  ATTENZIONE: i due metodi differiscono di oltre il 10%. Da annotare in decisioni.md.")
    else:
        print("  I due metodi coincidono (differenza sotto il 10%).")


def main():
    CARTELLA_OUTPUT.mkdir(exist_ok=True)
    controllo_iniziale()

    oggi = date.today().isoformat()
    righe = []
    # None = nessun filtro di paese = "Mondo"
    elenco_paesi = {**PAESI, "Mondo": None}

    totale = len(elenco_paesi) * len(ANNI) * len(TIPI)
    fatte = 0
    for nome, paese_api in elenco_paesi.items():
        for anno in ANNI:
            for tipo in TIPI:
                n = conta_studi(tipo, anno, paese_api)
                righe.append(
                    {
                        "paese": nome,
                        "anno": anno,
                        "tipo": tipo,
                        "n_studi": n,
                        "data_estrazione": oggi,
                    }
                )
                fatte += 1
                time.sleep(PAUSA)
        print(f"{nome}: completato ({fatte}/{totale} richieste)")

    df = pd.DataFrame(righe)
    percorso = CARTELLA_OUTPUT / "conteggi_paesi_anno.csv"
    df.to_csv(percorso, index=False, encoding="utf-8")
    print(f"\nSalvato: {percorso} ({len(df)} righe)")


if __name__ == "__main__":
    main()
