# MSC-ADHD-P05 — EEG Muse S Athena zsynchronizowane ze zdarzeniami regulacji

**Program:** `arc-neuro` · **obszar:** `ndd` · **rodzaj:** `MANUSCRIPT` · **etap rejestrowy szkicu:** `ACTIVE`.

Właścicielem naukowym i autorem obecnego szkicu jest Mateusz Pomianek (`MatPomGit`). Projekt i repozytorium kanoniczne pozostają niepotwierdzone. Publiczny katalog ARC dokumentuje koncepcję, lecz nie zastępuje protokołu ani rejestru dowodów projektu źródłowego.

## Projekt badania

**Przedmiot:** EEG Muse S Athena zsynchronizowane ze zdarzeniami regulacji.

- **Proponowany wynik główny:** Nie został zatwierdzony. Rozkład błędu czasowego znaczników i odsetek utraconych okien EEG są jedynie kandydatami na techniczne miary jakości. Estymand, jednostkę analizy oraz kryteria akceptacji należy zatwierdzić przed akwizycją.
- **Zakres i odrębność:** Wymaga odrębnego przeglądu nowości i porównania ze źródłowym protokołem.
- **Metodologia:** hipotezy, dobór próby lub scenariuszy, kryteria jakości, plan statystyczny i analiza wrażliwości wymagają potwierdzenia we właściwym projekcie. Ten plik nie potwierdza uzyskania wyników.
- **Powiązane MSC:** brak jawnego powiązania w rejestrze.

## Stan dowodów i weryfikacji

W repozytorium dostępny jest szkic LaTeX, plan metod i opis postulowanych zależności. Nie ma w publicznych rejestrach `portfolio/projects.json` i `portfolio/papers.json` wpisu wskazującego projekt źródłowy tego manuskryptu. Brak wskazanego źródła uniemożliwia potwierdzenie stanu `CURRENT` lub `STALE` względem kanonicznej rewizji. Nie zweryfikowano zapisu EEG, synchronizacji, integracji aplikacji, danych uczestników ani wyników. Rejestr `ACTIVE` opisuje organizacyjny stan szkicu, a nie wykonanie badania.

## Stanowisko badawcze

**`ST-01`**. Klasyfikacja `PROPOSED_BY_SCOPE`; kwalifikacja aparatury `NOT_VERIFIED`. Jest to propozycja organizacyjna, nie dowód gotowości stanowiska.

## Aplikacje

- **`app-regulation-mobile`** (`APP-ARC-02`): rola `PRIMARY`, decyzja `SOURCE_VALIDATION`; status repozytorium `PLANNED_NOT_CREATED`.
- **`app-eeg-neurolyze`** (`APP-ARC-03`): rola `SIGNAL_SOURCE`, decyzja `DEVICE_RIGHTS`; status repozytorium `ALTERNATE_EXISTING_APP`, istniejący odpowiednik `eeg-neurolyze`.

## Biblioteki

- **`lib-adapt`**: status `PLANNED_NOT_CREATED`, proponowana zależność przez `app-regulation-mobile`. Brak potwierdzonej integracji.
- **`lib-events`**: status `PLANNED_NOT_CREATED`, proponowana zależność przez `app-regulation-mobile`, `app-eeg-neurolyze`. Brak potwierdzonej integracji.
- **`lib-sig`**: status `RENAMED_PARTIAL_CORE`, proponowana zależność przez `app-eeg-neurolyze`. Brak potwierdzonej integracji.
- **`lib-sim`**: status `PLANNED_NOT_CREATED`, proponowana zależność przez `app-eeg-neurolyze`. Brak potwierdzonej integracji.

## Proweniencja i warunki realizacji

Szczegółowa proweniencja materiałów źródłowych, odwołania do repozytoriów niepublicznych i numery rewizji są przechowywane poza publiczną kartą.

Przed wykonaniem badania należy sprawdzić prawa do danych, kompletność protokołu, zgodę etyczną (jeżeli dotyczy), bezpieczeństwo aparatury oraz niezależność wyniku wobec innych manuskryptów. Wpisy biblioteczne i aplikacyjne są **planem**, nie deklaracją działającego API. Brak wyników oznacza `NOT_VERIFIED`, a nie wynik zerowy.
