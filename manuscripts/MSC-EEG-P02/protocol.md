# Protokół kwalifikacji technicznej

MSC-EEG-P02 · 1.0.0 · Mateusz Pomianek. Źródło oprogramowania to [Neurolyze, fb9191f](https://github.com/MatPomGit/eeg-neurolyze/tree/fb9191f2710f642f91b2de60adfaba527a239496). Procedura fizyczna i karta obserwacji pozostają w repozytorium źródłowym, odpowiednio w [runbooku M03](https://github.com/MatPomGit/eeg-neurolyze/blob/fb9191f2710f642f91b2de60adfaba527a239496/docs/research/2026-10-16-athena-hardware-validation-runbook.md) i [arkuszu M03](https://github.com/MatPomGit/eeg-neurolyze/blob/fb9191f2710f642f91b2de60adfaba527a239496/docs/research/2026-10-16-athena-hardware-validation-worksheet.md).

| Poziom | Wymagany dowód | Stan |
| --- | --- | --- |
| Oprogramowanie | Kwalifikacja typu wejścia, obsługa znaczników, indeksy strumienia | 7 testów offline PASS |
| Powtarzalność akwizycji | Trzy niezależne próby 60 s na backend i obsługiwaną konfigurację | NOT MEASURED |
| Zegar i zdarzenia | Znaczniki referencyjne, offset, dryf, rozkład reszt | NOT MEASURED |
| Kanały i sygnał | Kanały, jednostki, referencja, porównanie z wzorcem | NOT MEASURED |
| Zbiór EEG-BIDS | Oficjalny walidator i odczyt kontrolny konkretnego uprawnionego zbioru fizycznego | NOT VERIFIED |

Jednostką obserwacji jest rozpoczęta próba. W tabeli prób zapisać identyfikator lokalny sesji, konfigurację, backend, planowany czas, przedział obserwowany, podstawę zegara, poprawność archiwum, liczbę poprawnych próbek i status zakończenia. Każdy licznik ma wskazywać źródło, jednostkę i okres oceny. Dla porównań czasowych zapisać też zdarzenie referencyjne, sposób dopasowania, okno dopasowania i niepewność wzorca. Wzorzec i tor sprzętowy weryfikować bez uczestników. Nie publikować surowego BLE, śladów EEG ani adresów sprzętowych.

Przed rozpoczęciem zatwierdzić wzorzec, scenariusz, ryzyko tolerowane dla danego zastosowania i kolejność bloków. Presety inne niż podstawowy mają zastosowanie tylko po potwierdzeniu wsparcia firmware. Analizować wynik każdej konfiguracji, raportować nieudane próby oraz wersje środowiska. Błędy utraty ramek i braki danych oddzielać od niedostępności znacznika referencyjnego. Próby są zbyt małe do wnioskowania o niezawodności wszystkich egzemplarzy. Dłuższe przebiegi kwalifikacyjne wymagają oddzielnego projektu liczebności.

Kontrolę offline odtwarzają testy źródłowe `test_hardware_validation.py`, `test_measured_duplicate_timestamps.py` i `test_athena_index_continuity.py`. Każdy uruchamia się oddzielnie poleceniem `PYTHONPATH=src python -B -m unittest discover -s tests -p 'NAZWA.py'` z katalogu Neurolyze. Oczekiwana liczba przypadków wynosi odpowiednio 2, 2 i 3.
