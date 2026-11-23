# Walidacja szkicu MSC-ADHD-P03, etap 10/10

Data przeglądu: 2026-11-23. Dotyczy wyłącznie szkicu `MSC-ADHD-P03`.

## Identyfikowalność materiału

- Repozytorium i gałąź: `MatPomGit/arc-neuro`, `work/arc-articles-batch`.
- Bazowy commit przed kontrolą: `8b54859f76ae713a9d4c49ffc7d99ba140c5dab3`.
- Kontrolowany plik `main.tex`: blob SHA `b9e606e874f7ad247a4df91eaaf6b470d70f373c` (wersja tekstu `0.9.0`).
- Po kontroli zmieniono wyłącznie kartę tego artykułu `study.md`, aby uzgodnić opis proponowanego punktu końcowego; commit `93449e3426533e826ba5b8bd9beb5ced16d81071`. Plik `main.tex` pozostał bez zmian.

## Wyniki dostępnych kontroli

| Kontrola | Wynik | Zakres dowodu |
| --- | --- | --- |
| Odczyt HEAD, AGENTS.md, metadanych programu, portfolio, lokalnej karty i manuskryptu | PASS | Odczyt z GitHub dla wskazanej gałęzi |
| Bilans nawiasów klamrowych (z uwzględnieniem sekwencji sterujących, komentarzy i `\\verb`) | PASS | Statyczne sprawdzenie zawartości `main.tex` |
| Bilans i kolejność środowisk `\\begin` / `\\end` | PASS | 7 otwarć i 7 zamknięć, bez wykrytych niezgodności |
| Odwołania `\\label` / `\\ref` | PASS | 3 unikatowe etykiety i 3 istniejące cele odsyłaczy |
| Cytowania i plik bibliografii | INCOMPLETE | Nie ma cytowań ani pliku `.bib`; nie istnieją rekordy do sprawdzenia, a przegląd źródeł pozostaje do wykonania |
| Oznaczenia wyników | PASS | Dwie tabele i jedna rycina są wyraźnymi szablonami bez danych empirycznych |
| Oświadczenia etyczne, dane, kod, prerejestracja, finansowanie i jawność | PASS w zakresie tekstu | Brak niepotwierdzonych deklaracji zatwierdzenia badania, wyników, finansowania lub dostępu do danych |
| Linki do SPIRIT 2025, CONSORT 2025 i rozszerzenia dla pilotaży | PASS | Potwierdzono tożsamość wskazanych publikacji w indeksowanych źródłach publicznych |
| Zgodność opisu punktu końcowego w `study.md` i `main.tex` | CORRECTED | Wcześniejsza karta nie odzwierciedlała kandydackiej miary opisanej w manuskrypcie |
| Uruchomienie `pdflatex` dla pełnego `main.tex` | NOT_RUN | Kompilator był dostępny lokalnie, lecz nie udało się pobrać pliku przez sieć do środowiska kompilacji |
| Uwierzytelniony `audit-live` i odtwarzanie eksperymentu | NOT_RUN | Nie wykonano kodu z projektów zewnętrznych ani analizy empirycznej |

Kontrole statyczne nie zastępują kompilacji LaTeX, weryfikacji poprawności typograficznej PDF ani niezależnej recenzji metodologicznej. Nie ma podstaw do deklarowania gotowości publikacyjnej, prerejestracji ani przeprowadzonych pomiarów.

## Otwarte warunki przed przyszłym badaniem i publikacją

Należy potwierdzić repozytorium kanoniczne i uprawnienia, zweryfikować literaturę oraz opracować bibliografię APA 7, zamknąć definicję estymandu i protokołu, ustalić wymogi etyczne, uzyskać dowody walidacji aparatury i odtworzyć kompilację na dokładnym SHA. Po uzyskaniu danych konieczne będą udokumentowane analizy na przypiętych wersjach narzędzi. Do czasu ich przeprowadzenia status prac pozostaje `source_written`, a nie `tested` ani `published`.

Niniejszy raport dotyczy tylko jakości i spójności obecnego szkicu. Nie stanowi decyzji o scaleniu, publikacji ani rozpoczęciu rekrutacji.
