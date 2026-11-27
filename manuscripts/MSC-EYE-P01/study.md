# MSC-EYE-P01 — Trafność punktowego pomiaru spojrzenia z kamery Android: kalibracja i powtarzalność

**Program:** `arc-neuro` · **obszar:** `gaze-measurement-validity` · **rodzaj:** `MANUSCRIPT` · **etap źródłowy:** `PLANNED`.

## Projekt badania

**Przedmiot:** Trafność punktowego pomiaru spojrzenia z kamery Android: kalibracja i powtarzalność.

- **Proponowany wynik główny:** Błąd punktowy w pikselach/kącie oraz powtarzalność na sesjach testowych
- **Zakres i odrębność:** Metrologiczna dokładność/precision estymacji punktu; nie klasyfikacja regionów w grze.
- **Metodologia:** hipotezy, dobór próby lub scenariuszy, kryteria jakości, plan statystyczny i analiza wrażliwości wymagają potwierdzenia we właściwym projekcie. Ten plik nie potwierdza uzyskania wyników.
- **Powiązane MSC:** `MSC-EYE-P03`.

## Stanowisko badawcze

**`ST-02`**. Klasyfikacja `PROPOSED_BY_SCOPE`; kwalifikacja aparatury `NOT_VERIFIED`. Jest to propozycja organizacyjna, nie dowód gotowości stanowiska.

## Aplikacje

- **`app-eye-mobile`** (`APP-ARC-04`): rola `PRIMARY`, decyzja `MVP`; status repozytorium `PLANNED_NOT_CREATED`.

## Biblioteki

- **`lib-events`**: status `PLANNED_NOT_CREATED`, proponowana zależność przez `app-eye-mobile`. Brak potwierdzonej integracji.
- **`lib-eye`**: status `SCAFFOLD_EXISTS`, proponowana zależność przez `app-eye-mobile`. Brak potwierdzonej integracji.
- **`lib-vis`**: status `RENAMED_ARCHITECTURE_ONLY`, proponowana zależność przez `app-eye-mobile`. Brak potwierdzonej integracji.

## Proweniencja i warunki realizacji

Źródłowe materiały rozwija publiczny projekt [`arc-mobile-eyetracking`](https://github.com/MatPomGit/arc-mobile-eyetracking); oryginalny identyfikator `P01`.

Przed wykonaniem badania należy sprawdzić prawa do danych, kompletność protokołu, zgodę etyczną (jeżeli dotyczy), bezpieczeństwo aparatury oraz niezależność wyniku wobec innych manuskryptów. Wpisy biblioteczne i aplikacyjne są **planem**, nie deklaracją działającego API. Brak wyników oznacza `NOT_VERIFIED`, a nie wynik zerowy.
