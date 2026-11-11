# Registro delle decisioni – Progetto 4: l'Italia nella ricerca clinica

Incarico (simulato): la direttrice Affari Istituzionali chiede se l'Italia sta perdendo studi clinici rispetto a Spagna, Francia e Germania, con dati utilizzabili per un incontro con il Ministero.

## Decisioni prese da Manuel
| # | Tema | Decisione | Motivo |
|---|------|-----------|--------|
| 1 | Tipo di studio | Interventistici e osservazionali | Misurare tutta l'attività di ricerca registrata |
| 2 | Anno di riferimento | Anno di prima registrazione | Misura quando lo studio diventa visibile nel registro |
| 3 | Periodo | Una decade | Confrontare un periodo lungo e non un singolo anno |
| 4 | Fonte dati | API di ClinicalTrials.gov (v2) | Il sito AACT richiede un account per i download |

## Scelte dell'AI da confermare (da rivedere e approvare)
| # | Tema | Proposta | Motivo |
|---|------|----------|--------|
| 5 | Periodo preciso | 2016-2025 | Ultimi 10 anni completi; il 2026 è ancora in corso |
| 6 | Definizione di "Italia" | Studio con almeno una sede in Italia | Definizione standard, uguale per i quattro paesi e quindi confrontabile |
| 7 | Serie di controllo | Totale mondiale per anno | Distingue un calo dell'Italia da un calo generale del registro |
| 8 | Separazione dei tipi | Interventistici e osservazionali tenuti separati nel CSV | Permette di vedere se il trend dipende da un solo tipo |

## Risultati e decisioni dopo l'analisi (11/11/2026)
| # | Tema | Decisione | Motivo |
|---|------|-----------|--------|
| 9 | Misura principale per Elena | Studi interventistici | Quota dell'Italia sul mondo stabile (3,9% → 4,0%); Francia e Germania calano. Le serie sono confrontabili tra paesi |
| 10 | Studi osservazionali | Riportati a parte, con avvertenza | Il +241% dell'Italia dipende da registrazioni in blocco di pochi ospedali/IRCCS (Gemelli: 12 studi nel 2022, 197 nel 2023, di cui circa 150 tra gennaio e marzo; Bologna AOU: 162 nel 2024; San Matteo Pavia: 80 nel 2025). Gli altri sponsor restano stabili (339, 320, 387, 424, 347 dal 2021 al 2025) |
| 11 | Titolo del messaggio | "Non emerge un calo dell'Italia" e non "l'Italia cresce" | La crescita degli osservazionali è un effetto di registrazione, non di attività |

Verifica fatta: il filtro per paese e la ricerca libera danno lo stesso numero (1.105 studi interventistici italiani del 2020). I due metodi sono entrambi dell'API, quindi non è una verifica indipendente.

## Ipotesi non verificate (da non presentare come fatti)
- Il calo di Francia e Germania potrebbe dipendere da uno spostamento delle registrazioni verso altri registri europei. Non c'è prova nei dati.
- Nel 2023 in Italia c'è stata una riorganizzazione dei comitati etici (decreti ministeriali di gennaio 2023, 40 comitati territoriali). Potrebbe aver cambiato le abitudini di registrazione degli studi osservazionali, ma non ho trovato una fonte che colleghi le due cose.
- La classificazione "ospedali/istituti" è stata fatta con una ricerca sul nome dello sponsor ed è approssimativa.

## Cosa non sappiamo (da dichiarare nella nota a Elena)
- Non conosciamo la causa del calo di Francia e Germania negli studi interventistici.
- Il numero di studi registrati non coincide con l'attività di ricerca reale: dipende anche da quanto e quando si registra.
- Per gli osservazionali la registrazione è in genere volontaria, quindi la serie riflette le scelte dei singoli enti.
- Test di robustezza (script 04): Gemelli, San Raffaele e Auxologico spiegano 297 dei 508 studi osservazionali in più del 2023 rispetto al 2022 (58%). Senza di loro l'aumento è +49% invece di +110%; fino al 2025 è +77% invece di +94%. Il resto della crescita è comunque concentrato in altri grandi ospedali (Bologna AOU nel 2024, San Matteo di Pavia nel 2025): non possiamo dire se sia attività reale o altre registrazioni in blocco.

## Punto aperto da girare alla direttrice
- **Sponsor italiano.** Nell'API non esiste il paese dello sponsor, solo nome e categoria (industria, università, ente pubblico…). Filtrare "sede in Italia e sponsor italiano" richiederebbe di classificare a mano migliaia di sponsor, per tutti e quattro i paesi. Proposta: misura principale per sede, e come approfondimento la ripartizione per categoria di sponsor (industria contro non industria).

## Limiti noti
- Uno studio multicentrico è contato in ogni paese in cui ha sedi: le serie dei paesi non si sommano.
- L'API è aggiornata ogni giorno: ogni numero va citato con la data di estrazione.
- Le abitudini di registrazione cambiano nel tempo: un calo nel registro non è necessariamente un calo nell'attività reale.

## Verifiche fatte
- [x] Controllo iniziale: il filtro per paese coincide con la ricerca libera (script 01): 1.105 = 1.105
- [x] Controllo sul sito clinicaltrials.gov (11/11/2026): studi interventistici con sede in Italia nel 2020 = 1.105, uguale al conteggio dell'API. È la verifica indipendente
- [ ] Altri 1-2 conteggi controllati sul sito (per esempio un altro paese o un altro anno)
- [ ] Conteggio del mondo coerente con il totale degli studi registrati
