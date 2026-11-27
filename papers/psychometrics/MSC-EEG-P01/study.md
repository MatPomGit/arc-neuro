# MSC-EEG-P01 — Kandydat: publikacja metod oprogramowania EEG Neurolyze

**Program:** `arc-neuro` · **obszar:** `eeg-measurement-workflow-reproducibility` · **rodzaj:** `IDEA` · **etap źródłowy:** `PROPOSED`.

## Projekt badania

**Przedmiot:** Kandydat: publikacja metod oprogramowania EEG Neurolyze.

- **Proponowany wynik główny:** Zgodność PSD i mocy alfa z SciPy w 18 syntetycznych przypadkach o jawnych parametrach.
- **Zakres i odrębność:** Weryfikacja oprogramowania. Kwalifikacja urządzenia pozostaje w MSC-EEG-P02.
- **Metodologia:** hipotezy, dobór próby lub scenariuszy, kryteria jakości, plan statystyczny i analiza wrażliwości wymagają potwierdzenia we właściwym projekcie. Ten plik nie potwierdza uzyskania wyników.
- **Powiązane MSC:** brak jawnego powiązania w rejestrze.

## Stanowisko badawcze

**`ST-01`**. Klasyfikacja `PROPOSED_BY_SCOPE`; kwalifikacja aparatury `NOT_VERIFIED`. Jest to propozycja organizacyjna, nie dowód gotowości stanowiska.

## Aplikacje

- **`app-eeg-neurolyze`** (`APP-ARC-03`): rola `PRIMARY`, decyzja `SOURCE_VALIDATION`; status repozytorium `ALTERNATE_EXISTING_APP`, istniejący odpowiednik `eeg-neurolyze`.

## Biblioteki

- **`lib-events`**: status `PLANNED_NOT_CREATED`, proponowana zależność przez `app-eeg-neurolyze`. Brak potwierdzonej integracji.
- **`lib-sig`**: status `RENAMED_PARTIAL_CORE`, proponowana zależność przez `app-eeg-neurolyze`. Brak potwierdzonej integracji.
- **`lib-sim`**: status `PLANNED_NOT_CREATED`, proponowana zależność przez `app-eeg-neurolyze`. Brak potwierdzonej integracji.

## Proweniencja i warunki realizacji

Źródłowe materiały rozwija publiczny projekt [`eeg-neurolyze`](https://github.com/MatPomGit/eeg-neurolyze); oryginalny identyfikator `software-methods`.

Przed wykonaniem badania należy sprawdzić prawa do danych, kompletność protokołu, zgodę etyczną (jeżeli dotyczy), bezpieczeństwo aparatury oraz niezależność wyniku wobec innych manuskryptów. Wpisy biblioteczne i aplikacyjne są **planem**, nie deklaracją działającego API. Brak wyników oznacza `NOT_VERIFIED`, a nie wynik zerowy.
