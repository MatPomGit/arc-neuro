# MSC-DERA-P01 — Struktura czynnikowa i trafność narzędzia DERA-HRI do oceny doświadczenia interakcji z humanoidem

**Właściciel naukowy i autor szkicu:** Mateusz Pomianek (`MatPomGit`). Współautorów należy wskazywać zgodnie z potwierdzonym wkładem; repozytorium kanoniczne jest odrębną informacją.

**Rodzaj pracy:** `IDEA`. **Etap badań:** `CANDIDATE_VALIDATION_DATA_REQUIRED`.

[Manuskrypt LaTeX](main.tex) zawiera odrębny tytuł, pytanie badawcze i projekt analizy. Jest to szkic badawczy; brak w nim niezweryfikowanych wyników empirycznych.

Temat i status odpowiadają jednoznacznemu identyfikatorowi MSC w rejestrze portfolio. Materiały źródłowe i dowody eksperymentalne zachowują właściciela we właściwym projekcie badawczym.

## Pakiet prospektywny 1.0.0

[Protokół walidacji](protocol.md) obejmuje pochodzenie instrumentu, wywiady poznawcze, niezależne próby eksploracyjną i konfirmacyjną, analizę inwariancji i plan danych. [Bibliografia](references.bib) dokumentuje podstawy psychometryczne i komparatory HRI.

Zbudowanie PDF: `latexmk -norc -pdf main.tex`. Syntetyczną symulację ryzyka rzadkich kategorii (zależności w `requirements.txt`, [wyniki](category-risk.csv)) odtwarza `python3 simulation.py > category-risk.csv`.
