"""
02_analisi.py  (versione 2: analisi divisa per tipo di studio)

Legge output/conteggi_paesi_anno.csv e, per ciascuna delle tre viste
(interventistici, osservazionali, tutti), produce:
- output/tabella_<vista>.csv: studi per anno e paese, quota sul mondo e indice base 2016=100
- output/grafico_<vista>_indice.png: andamento con indice 2016=100
- output/grafico_<vista>_quota.png: quota % sul totale mondiale
e stampa un riepilogo (primo triennio contro ultimo triennio).

Perche' tre viste: i risultati cambiano molto a seconda del tipo di studio.
Gli INTERVENTISTICI sono la misura piu' confrontabile tra paesi; gli osservazionali dipendono
molto dalle abitudini locali di registrazione. "Tutti" nasconde le differenze, quindi va letto
solo insieme alle altre due.

Le serie dei paesi NON si sommano: uno studio multicentrico compare in piu' paesi.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

CARTELLA_OUTPUT = Path(__file__).resolve().parent.parent / "output"
PAESI = ["Italia", "Spagna", "Francia", "Germania"]
ANNO_BASE = 2016
VISTE = {
    "interventistici": ["INTERVENTIONAL"],
    "osservazionali": ["OBSERVATIONAL"],
    "tutti": ["INTERVENTIONAL", "OBSERVATIONAL"],
}


def prepara_tabelle(df, tipi):
    """Restituisce (studi, quota sul mondo in %, indice base 2016=100) per i tipi indicati."""
    parte = df[df["tipo"].isin(tipi)]
    totale = parte.groupby(["paese", "anno"], as_index=False)["n_studi"].sum()
    studi = totale.pivot(index="anno", columns="paese", values="n_studi")
    quota = studi[PAESI].div(studi["Mondo"], axis=0) * 100
    indice = studi.div(studi.loc[ANNO_BASE]) * 100
    return studi, quota, indice


def grafico_indice(indice, titolo, percorso, data_estrazione):
    fig, ax = plt.subplots(figsize=(9, 5))
    for nome in PAESI:
        ax.plot(indice.index, indice[nome], marker="o", linewidth=3 if nome == "Italia" else 1.5, label=nome)
    ax.plot(indice.index, indice["Mondo"], linestyle="--", color="grey", label="Mondo")
    ax.axhline(100, color="black", linewidth=0.5)
    ax.set_title(f"{titolo}: studi registrati per anno, indice {ANNO_BASE}=100")
    ax.set_ylabel(f"Indice ({ANNO_BASE}=100)")
    ax.set_xlabel("Anno di registrazione (studi con almeno una sede nel paese)")
    ax.legend()
    fig.text(0.01, 0.01, f"Fonte: ClinicalTrials.gov, estrazione del {data_estrazione}", fontsize=8)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(percorso, dpi=150)
    plt.close(fig)


def grafico_quota(quota, titolo, percorso, data_estrazione):
    fig, ax = plt.subplots(figsize=(9, 5))
    for nome in PAESI:
        ax.plot(quota.index, quota[nome], marker="o", linewidth=3 if nome == "Italia" else 1.5, label=nome)
    ax.set_title(f"{titolo}: quota % degli studi mondiali con almeno una sede nel paese")
    ax.set_ylabel("% sul totale mondiale")
    ax.set_xlabel("Anno di registrazione")
    ax.legend()
    fig.text(0.01, 0.01, f"Fonte: ClinicalTrials.gov, estrazione del {data_estrazione}", fontsize=8)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(percorso, dpi=150)
    plt.close(fig)


def main():
    df = pd.read_csv(CARTELLA_OUTPUT / "conteggi_paesi_anno.csv")
    data_estrazione = df["data_estrazione"].iloc[0]
    print(f"Dati estratti il {data_estrazione}")

    for vista, tipi in VISTE.items():
        studi, quota, indice = prepara_tabelle(df, tipi)

        tabella = pd.concat(
            {"studi": studi, "quota_mondo_%": quota.round(2), f"indice_{ANNO_BASE}=100": indice.round(1)},
            axis=1,
        )
        tabella.to_csv(CARTELLA_OUTPUT / f"tabella_{vista}.csv", encoding="utf-8")

        # Primo triennio contro ultimo triennio: attenua le oscillazioni di un singolo anno
        primo, ultimo = studi.iloc[:3].mean(), studi.iloc[-3:].mean()
        variazione = ((ultimo / primo - 1) * 100).round(1)
        quota_primo, quota_ultimo = quota.iloc[:3].mean().round(2), quota.iloc[-3:].mean().round(2)
        riepilogo = pd.DataFrame(
            {"variazione_%": variazione, "quota_primo_3anni_%": quota_primo, "quota_ultimo_3anni_%": quota_ultimo}
        )
        print(f"\n=== {vista.upper()} (media annua, ultimo triennio contro primo) ===")
        print(riepilogo.to_string())

        grafico_indice(indice, vista.capitalize(), CARTELLA_OUTPUT / f"grafico_{vista}_indice.png", data_estrazione)
        grafico_quota(quota, vista.capitalize(), CARTELLA_OUTPUT / f"grafico_{vista}_quota.png", data_estrazione)

    print(f"\nFile salvati in {CARTELLA_OUTPUT}")


if __name__ == "__main__":
    main()
