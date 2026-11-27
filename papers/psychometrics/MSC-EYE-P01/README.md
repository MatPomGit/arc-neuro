# MSC-EYE-P01 — Trafność punktowego pomiaru spojrzenia z kamery Android: kalibracja i powtarzalność

**Właściciel naukowy i autor szkicu:** Mateusz Pomianek (`MatPomGit`). Współautorów należy wskazywać zgodnie z potwierdzonym wkładem; repozytorium kanoniczne jest odrębną informacją.

**Rodzaj pracy:** `MANUSCRIPT`. **Etap badań:** `PLANNED`.

[Manuskrypt LaTeX](main.tex) zawiera odrębny tytuł, pytanie badawcze i projekt analizy. Jest to szkic badawczy; brak w nim niezweryfikowanych wyników empirycznych.

Temat i status odpowiadają jednoznacznemu identyfikatorowi MSC w rejestrze portfolio. Materiały źródłowe i dowody eksperymentalne zachowują właściciela we właściwym projekcie badawczym.

## Pakiet 1.0.0

[Protokół E01](protocol.md), [LaTeX](main.tex) i [przykład syntetyczny](geometry-synthetic.csv). Odtworzenie geometrii: `python -B geometry.py`. Testy: `python -B -m unittest -v`. PDF buduje `latexmk -norc -pdf main.tex`.
