# MSC-EEG-P02 — plan badania i powiązania

**Temat:** Kandydat: walidacja techniczna urządzeń EEG w EEG Neurolyze

**Program:** `arc-neuro`. **Obszar:** `eeg-device-qualification`. **Typ:** `IDEA` (CANDIDATE). **Stan źródła:** `PROPOSED`. **Tryb integracji:** `INDEX_ONLY_NO_NEW_FOLDER`.

## Cel, wynik główny i granice badania

Przedmiot badania: Kandydat: walidacja techniczna urządzeń EEG w EEG Neurolyze. Kandydatura, bez zatwierdzonego odrębnego protokołu.

- **Główny wynik proponowany:** Nieokreślony w rejestrze. Wymaga zdefiniowania metryki, estymandu i jednostki analizy przed rozpoczęciem badania.
- **Odrębność naukowa:** Należy porównać źródłowy protokół z pokrewnymi manuskryptami przed formalizacją hipotezy.
- **Uzasadnienie klasyfikacji:** Proposal w PROJECT_STATE.yaml (issue #35); hardware qualification, brak ukończonych pomiarów i tytułu, manuscript_path=null. Nie promować testów syntetycznych jako danych empirycznych. [Klasyfikacja portfolio 2026-11-20] Planowana walidacja metrologiczna urządzeń EEG i jakości akwizycji; nie jest pracą nad nowym modelem AI. Brak pomiarów sprzętowych; nie wnioskować o jakości urządzenia z testów syntetycznych.
- **Powiązane rekordy:** Nie zarejestrowano.

## Stanowisko badawcze

**Wstępne powiązanie:** `ST-01`. To propozycja na podstawie domeny, a nie potwierdzenie uruchomienia aparatury.

[Stanowiska ARC](https://github.com/MatPomGit/research-autopilot/blob/main/docs/portfolio/reorganizacja-systemu-badan/shared_research_platforms.md); [inwentarz prywatny `devices`](https://github.com/MatPomGit/devices).

## Powiązane aplikacje APP

- `app-eeg-neurolyze` (`APP-ARC-03`), `PRIMARY`, profil `python-eeg`, bramka `SOURCE_VALIDATION`.

## Powiązane biblioteki LIB

- `lib-events`: planowana zależność pośrednia przez `app-eeg-neurolyze`; brak dowodu integracji.
- `lib-signals` (historyczna nazwa; wymaga uzgodnienia z `lib-sig`): planowana zależność pośrednia przez `app-eeg-neurolyze`; brak dowodu integracji.
- `lib-sim`: planowana zależność pośrednia przez `app-eeg-neurolyze`; brak dowodu integracji.

Relacje APP i LIB pochodzą odpowiednio z `app_publication_links.csv` i `component_dependencies.csv`. Są kandydaturami, nie dowodami wykonania prac. Aktualność nazw `lib-signals`, `lib-image` i `lib-llm` wymaga osobnego uzgodnienia z nowymi repozytoriami.

## Proweniencja, metodologia i bramki

- **UID źródłowy:** `eeg-neurolyze:device-qualification`; repozytorium `MatPomGit/eeg-neurolyze`, identyfikator `device-qualification`.
- **Ścieżka źródłowa:** `PROJECT_STATE.yaml`.
- **Materiał:** [źródło projektu](https://github.com/MatPomGit/eeg-neurolyze/blob/main/PROJECT_STATE.yaml).
- **Rejestr MSC:** [kanoniczna macierz](https://github.com/MatPomGit/research-autopilot/blob/main/docs/portfolio/reorganizacja-systemu-badan/publication_matrix.csv).

Przed badaniem wymagane są niezależny wynik i plan analizy, źródła literaturowe, ocena nowości, kontrola praw do danych/oprogramowania, ocena bezpieczeństwa i kwalifikacja etyczna, jeżeli dotyczy. Szkic nie zawiera danych empirycznych ani nie potwierdza dostępności stanowiska.
