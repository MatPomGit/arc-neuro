# MSC-EEG-P02 — Kandydat: walidacja techniczna urządzeń EEG w EEG Neurolyze

**Program:** `arc-neuro` · **obszar:** `eeg-device-qualification` · **rodzaj:** `IDEA` · **etap źródłowy:** `PROPOSED`.

## Projekt badania

**Przedmiot:** Kandydat: walidacja techniczna urządzeń EEG w EEG Neurolyze.

- **Proponowany wynik główny:** Odsetek pełnych sesji technicznych spośród rozpoczętych prób w obrębie konfiguracji i backendu.
- **Zakres i odrębność:** Kwalifikacja pomiarowa urządzenia i metadanych względem niezależnego odniesienia. MSC-EEG-P01 obejmuje poprawność oprogramowania.
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

Źródłowe materiały rozwija publiczny projekt [`eeg-neurolyze`](https://github.com/MatPomGit/eeg-neurolyze); oryginalny identyfikator `device-qualification`.

Przed wykonaniem badania należy sprawdzić prawa do danych, kompletność protokołu, zgodę etyczną (jeżeli dotyczy), bezpieczeństwo aparatury oraz niezależność wyniku wobec innych manuskryptów. Wpisy biblioteczne i aplikacyjne są **planem**, nie deklaracją działającego API. Brak wyników oznacza `NOT_VERIFIED`, a nie wynik zerowy.
