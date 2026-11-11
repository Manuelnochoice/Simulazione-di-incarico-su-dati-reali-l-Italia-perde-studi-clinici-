"""
04_robustezza.py

Test di robustezza sugli studi OSSERVAZIONALI con sede in Italia (2021-2025).

Domanda: quanto dell'aumento 2022 -> 2023 dipende da tre soli enti
(Gemelli, San Raffaele, Auxologico)? Cosa resta se li escludiamo?

Legge output/italia_osservazionali_dettaglio.csv (creato da 03_salto_2023.py).
Salva output/robustezza_osservazionali.csv e stampa il confronto.

Nota: la scelta dei tre enti viene dai dati (maggiori incrementi 2022 -> 2023) ed e' una scelta
dell'analista. Il test mostra quanto pesano, non dimostra che le loro registrazioni siano anomale.
"""

from pathlib import Path

import pandas as pd

CARTELLA_OUTPUT = Path(__file__).resolve().parent.parent / "output"
ENTI = {
    "Gemelli": "Gemelli",
    "San Raffaele": "San Raffaele",
    "Auxologico": "Auxologico",
}


def main():
    df = pd.read_csv(CARTELLA_OUTPUT / "italia_osservazionali_dettaglio.csv")
    sponsor = df["sponsor"].fillna("")

    # Segno gli studi dei tre enti (ricerca del nome nello sponsor)
    df["tre_enti"] = False
    for parola in ENTI.values():
        df["tre_enti"] |= sponsor.str.contains(parola, case=False, regex=False)

    tabella = pd.DataFrame(
        {
            "totale": df.groupby("anno").size(),
            "tre_enti": df[df["tre_enti"]].groupby("anno").size(),
        }
    ).fillna(0).astype(int)
    tabella["senza_tre_enti"] = tabella["totale"] - tabella["tre_enti"]
    tabella.to_csv(CARTELLA_OUTPUT / "robustezza_osservazionali.csv", encoding="utf-8")

    print(tabella.to_string())

    def variazione(colonna, da, a):
        return (tabella.loc[a, colonna] / tabella.loc[da, colonna] - 1) * 100

    print("\nVariazione % 2022 -> 2023:")
    print(f"  totale:          {variazione('totale', 2022, 2023):+.0f}%")
    print(f"  senza tre enti:  {variazione('senza_tre_enti', 2022, 2023):+.0f}%")
    aumento_totale = tabella.loc[2023, "totale"] - tabella.loc[2022, "totale"]
    aumento_tre = tabella.loc[2023, "tre_enti"] - tabella.loc[2022, "tre_enti"]
    print(f"\nAumento assoluto 2022 -> 2023: {aumento_totale} studi, di cui {aumento_tre} "
          f"dai tre enti ({aumento_tre / aumento_totale * 100:.0f}%)")

    print("\nVariazione % 2022 -> 2025:")
    print(f"  totale:          {variazione('totale', 2022, 2025):+.0f}%")
    print(f"  senza tre enti:  {variazione('senza_tre_enti', 2022, 2025):+.0f}%")


if __name__ == "__main__":
    main()
