# MSC-EYE-P03 — Zgodność klasyfikacji regionów spojrzenia w mobilnej grze 2D przy zmianie warunków

**Program:** `arc-neuro` · **obszar:** `mobile-gaze-metrology` · **rodzaj:** `IDEA` · **etap źródłowy:** `IDEA_DEFINED`.

## Projekt badania

**Przedmiot:** Zgodność klasyfikacji regionów spojrzenia w mobilnej grze 2D przy zmianie warunków.

- **Proponowany wynik główny:** F1/zgodność klasyfikacji ROI w scenariuszach gry i zmiennych warunkach
- **Zakres i odrębność:** Metoda funkcjonalna ROI i brak przełączeń błędnych podczas gry; osobny outcome od punktowego błędu urządzenia P01.
- **Metodologia:** hipotezy, dobór próby lub scenariuszy, kryteria jakości, plan statystyczny i analiza wrażliwości wymagają potwierdzenia we właściwym projekcie. Ten plik nie potwierdza uzyskania wyników.
- **Powiązane MSC:** `MSC-EYE-P01`.

## Stanowisko badawcze

**`ST-02`**. Klasyfikacja `PROPOSED_BY_SCOPE`; kwalifikacja aparatury `NOT_VERIFIED`. Jest to propozycja organizacyjna, nie dowód gotowości stanowiska.

## Aplikacje

- **`app-2d-mobile`** (`APP-ARC-01M`): rola `PRIMARY`, decyzja `MVP`; status repozytorium `PLANNED_NOT_CREATED`.
- **`app-eye-mobile`** (`APP-ARC-04`): rola `SIGNAL_SOURCE`, decyzja `CROSS_PLATFORM`; status repozytorium `PLANNED_NOT_CREATED`.
- **`app-eye-desktop`** (`APP-ARC-05`): rola `COMPARATOR`, decyzja `CROSS_PLATFORM`; status repozytorium `PLANNED_NOT_CREATED`.

## Biblioteki

- **`lib-adapt`**: status `PLANNED_NOT_CREATED`, proponowana zależność przez `app-2d-mobile`. Brak potwierdzonej integracji.
- **`lib-events`**: status `PLANNED_NOT_CREATED`, proponowana zależność przez `app-2d-mobile`, `app-eye-mobile`, `app-eye-desktop`. Brak potwierdzonej integracji.
- **`lib-eye`**: status `SCAFFOLD_EXISTS`, proponowana zależność przez `app-2d-mobile`, `app-eye-mobile`, `app-eye-desktop`. Brak potwierdzonej integracji.
- **`lib-study`**: status `PLANNED_NOT_CREATED`, proponowana zależność przez `app-2d-mobile`. Brak potwierdzonej integracji.
- **`lib-vis`**: status `RENAMED_ARCHITECTURE_ONLY`, proponowana zależność przez `app-2d-mobile`, `app-eye-mobile`, `app-eye-desktop`. Brak potwierdzonej integracji.

## Proweniencja i warunki realizacji

Źródłowe materiały rozwija publiczny projekt [`arc-xr`](https://github.com/MatPomGit/arc-xr); oryginalny identyfikator `GAZE-METHOD`.

Przed wykonaniem badania należy sprawdzić prawa do danych, kompletność protokołu, zgodę etyczną (jeżeli dotyczy), bezpieczeństwo aparatury oraz niezależność wyniku wobec innych manuskryptów. Wpisy biblioteczne i aplikacyjne są **planem**, nie deklaracją działającego API. Brak wyników oznacza `NOT_VERIFIED`, a nie wynik zerowy.
