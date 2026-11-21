# MSC-SYNC-P04 — plan badania i powiązania

**Temat:** Przedziały niepewności synchronizacji smartfon–EEG przy dryfie i utracie pakietów

**Program:** `arc-neuro`. **Obszar:** `eeg-event-time-qualification`. **Typ:** `IDEA` (CANDIDATE). **Stan źródła:** `STOP_STANDALONE`. **Tryb integracji:** `INDEX_ONLY_NO_NEW_FOLDER`.

## Cel, wynik główny i granice badania

Przedmiot badania: Przedziały niepewności synchronizacji smartfon–EEG przy dryfie i utracie pakietów. Kandydatura, bez zatwierdzonego odrębnego protokołu.

- **Główny wynik proponowany:** Pokrycie nominalnych 95-proc. przedziałów niepewności czasu i ich szerokość względem niezależnej referencji zegarowej
- **Odrębność naukowa:** Metrologiczna kalibracja interwału czasu przy utracie pakietów, nie wpływ opóźnienia na wynik recovery w MSC-SYNC-P01. Źródłowe STOP_STANDALONE nadal obowiązuje do nowej oceny nowości.
- **Uzasadnienie klasyfikacji:** STOP jako samodzielny artykuł w obecnym wariancie; utrzymać pomysł jako metodę P05. [Klasyfikacja portfolio 2026-11-20] Przypisanie merytoryczne: walidacja synchronizacji smartfon–EEG jako infrastruktury pomiaru w P05. Zachować STOP_STANDALONE; nie planować niezależnego artykułu bez nowego estymatora i benchmarku. | Proponowane doprecyzowanie zakresu portfolio 2026-11-20, wymaga zatwierdzenia naukowego: Zachować źródłowy STOP_STANDALONE, nie wliczać do niezależnych kandydatur. Główny wynik do prerejestracji: Nie dotyczy samodzielnego artykułu: komponent metodyczny ADHD P05. Tytuł źródłowy zachowano w original_title_pl. | AUTORSKA PROPOZYCJA N
- **Powiązane rekordy:** `MSC-ADHD-P05` (arc-adhd-game:P05)

## Stanowisko badawcze

**Wstępne powiązanie:** `ST-00`. To propozycja na podstawie domeny, a nie potwierdzenie uruchomienia aparatury.

[Stanowiska ARC](https://github.com/MatPomGit/research-autopilot/blob/main/docs/portfolio/reorganizacja-systemu-badan/shared_research_platforms.md); [inwentarz prywatny `devices`](https://github.com/MatPomGit/devices).

## Powiązane aplikacje APP

- `app-regulation-mobile` (`APP-ARC-02`), `SIGNAL_SOURCE`, profil `android-native`, bramka `RESEARCH_GO`.
- `app-eeg-neurolyze` (`APP-ARC-03`), `SIGNAL_SOURCE`, profil `python-eeg`, bramka `DEVICE_RIGHTS`.

## Powiązane biblioteki LIB

- `lib-adapt`: planowana zależność pośrednia przez `app-regulation-mobile`; brak dowodu integracji.
- `lib-events`: planowana zależność pośrednia przez `app-regulation-mobile`, `app-eeg-neurolyze`; brak dowodu integracji.
- `lib-signals` (historyczna nazwa; wymaga uzgodnienia z `lib-sig`): planowana zależność pośrednia przez `app-eeg-neurolyze`; brak dowodu integracji.
- `lib-sim`: planowana zależność pośrednia przez `app-eeg-neurolyze`; brak dowodu integracji.

Relacje APP i LIB pochodzą odpowiednio z `app_publication_links.csv` i `component_dependencies.csv`. Są kandydaturami, nie dowodami wykonania prac. Aktualność nazw `lib-signals`, `lib-image` i `lib-llm` wymaga osobnego uzgodnienia z nowymi repozytoriami.

## Proweniencja, metodologia i bramki

- **UID źródłowy:** `arc-adhd-game:S01`; repozytorium `MatPomGit/arc-adhd-game`, identyfikator `S01`.
- **Ścieżka źródłowa:** `manuscripts/candidate_papers_gate_2026-11-11.md`.
- **Materiał:** [źródło projektu](https://github.com/MatPomGit/arc-adhd-game/blob/main/manuscripts/candidate_papers_gate_2026-11-11.md).
- **Rejestr MSC:** [kanoniczna macierz](https://github.com/MatPomGit/research-autopilot/blob/main/docs/portfolio/reorganizacja-systemu-badan/publication_matrix.csv).

Przed badaniem wymagane są niezależny wynik i plan analizy, źródła literaturowe, ocena nowości, kontrola praw do danych/oprogramowania, ocena bezpieczeństwa i kwalifikacja etyczna, jeżeli dotyczy. Szkic nie zawiera danych empirycznych ani nie potwierdza dostępności stanowiska.
