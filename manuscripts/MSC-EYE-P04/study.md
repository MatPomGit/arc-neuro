# MSC-EYE-P04 — Kiedy adaptacyjny interfejs powinien podpowiadać? Ostrożna adaptacja 2D oparta na jakości spojrzenia

**Program:** `arc-neuro` · **obszar:** `cognition` · **rodzaj:** `IDEA` · **etap źródłowy:** `IDEA_DEFINED`.

## Projekt badania

**Przedmiot:** Kiedy adaptacyjny interfejs powinien podpowiadać? Ostrożna adaptacja 2D oparta na jakości spojrzenia.

- **Proponowany wynik główny:** Nie określono dotychczas w rejestrze. Należy zdefiniować estymand, miarę i jednostkę analizy przed akwizycją.
- **Zakres i odrębność:** Wymaga odrębnego przeglądu nowości i porównania ze źródłowym protokołem.
- **Metodologia:** hipotezy, dobór próby lub scenariuszy, kryteria jakości, plan statystyczny i analiza wrażliwości wymagają potwierdzenia we właściwym projekcie. Ten plik nie potwierdza uzyskania wyników.
- **Powiązane MSC:** `MSC-EYE-P03`, `MSC-AFFECT-P06`.

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

Źródłowe materiały rozwija publiczny projekt [`arc-xr`](https://github.com/MatPomGit/arc-xr); oryginalny identyfikator `GAZE-EXPERIMENT`.

Przed wykonaniem badania należy sprawdzić prawa do danych, kompletność protokołu, zgodę etyczną (jeżeli dotyczy), bezpieczeństwo aparatury oraz niezależność wyniku wobec innych manuskryptów. Wpisy biblioteczne i aplikacyjne są **planem**, nie deklaracją działającego API. Brak wyników oznacza `NOT_VERIFIED`, a nie wynik zerowy.
