# MSC-DERA-P01 — Struktura czynnikowa i trafność narzędzia DERA-HRI do oceny doświadczenia interakcji z humanoidem

**Program:** `arc-neuro` · **obszar:** `dera-hri-psychometrics` · **rodzaj:** `IDEA` · **etap źródłowy:** `CANDIDATE_VALIDATION_DATA_REQUIRED`.

## Projekt badania

**Przedmiot:** Struktura czynnikowa i trafność narzędzia DERA-HRI do oceny doświadczenia interakcji z humanoidem.

- **Proponowany wynik główny:** Replikowalność modelu czynnikowego DERA-HRI na niezależnej próbie oraz przedziały dla rzetelności i trafności
- **Zakres i odrębność:** Psychometryczna walidacja skali, odrębna od zależności między subiektywnym i fizycznym bezpieczeństwem w MSC-HRI-P08.
- **Metodologia:** hipotezy, dobór próby lub scenariuszy, kryteria jakości, plan statystyczny i analiza wrażliwości wymagają potwierdzenia we właściwym projekcie. Ten plik nie potwierdza uzyskania wyników.
- **Powiązane MSC:** `INS-DERA-I01`, `MSC-HRI-P08`.

## Stanowisko badawcze

**`ST-07`**. Klasyfikacja `PROPOSED_BY_SCOPE`; kwalifikacja aparatury `NOT_VERIFIED`. Jest to propozycja organizacyjna, nie dowód gotowości stanowiska.

## Aplikacje

- **`app-study-web`** (`APP-ARC-06`): rola `OPTIONAL`, decyzja `RESEARCH_GO`; status repozytorium `PLANNED_NOT_CREATED`.
- **`app-hri-console`** (`APP-ARC-08`): rola `OPTIONAL`, decyzja `RESEARCH_GO`; status repozytorium `PLANNED_NOT_CREATED`.

## Biblioteki

- **`lib-audio`**: status `SCOPE_CONSOLIDATED_PLAN`, proponowana zależność przez `app-hri-console`. Brak potwierdzonej integracji.
- **`lib-events`**: status `PLANNED_NOT_CREATED`, proponowana zależność przez `app-study-web`, `app-hri-console`. Brak potwierdzonej integracji.
- **`lib-ros`**: status `SCAFFOLD_EXISTS`, proponowana zależność przez `app-hri-console`. Brak potwierdzonej integracji.
- **`lib-sim`**: status `PLANNED_NOT_CREATED`, proponowana zależność przez `app-hri-console`. Brak potwierdzonej integracji.
- **`lib-study`**: status `PLANNED_NOT_CREATED`, proponowana zależność przez `app-study-web`. Brak potwierdzonej integracji.
- **`lib-track`**: status `NEW_SCAFFOLD_EXISTS`, proponowana zależność przez `app-hri-console`. Brak potwierdzonej integracji.
- **`lib-vis`**: status `RENAMED_ARCHITECTURE_ONLY`, proponowana zależność przez `app-hri-console`. Brak potwierdzonej integracji.
- **`lib-vlm`**: status `SCAFFOLD_EXISTS`, proponowana zależność przez `app-study-web`, `app-hri-console`. Brak potwierdzonej integracji.

## Proweniencja i warunki realizacji

Szczegółowa proweniencja materiałów źródłowych, odwołania do repozytoriów niepublicznych i numery rewizji są przechowywane poza publiczną kartą.

Przed wykonaniem badania należy sprawdzić prawa do danych, kompletność protokołu, zgodę etyczną (jeżeli dotyczy), bezpieczeństwo aparatury oraz niezależność wyniku wobec innych manuskryptów. Wpisy biblioteczne i aplikacyjne są **planem**, nie deklaracją działającego API. Brak wyników oznacza `NOT_VERIFIED`, a nie wynik zerowy.
