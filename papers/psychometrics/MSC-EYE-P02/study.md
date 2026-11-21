# MSC-EYE-P02 — plan badania i powiązania

**Temat:** Selektor jakości gaze przy zmianie telefonu i warunków

**Program:** `arc-neuro`. **Obszar:** `gaze-measurement-validity`. **Typ:** `IDEA` (CANDIDATE). **Stan źródła:** `IDEA_HOLD`. **Tryb integracji:** `INDEX_ONLY_NO_NEW_FOLDER`.

## Cel, wynik główny i granice badania

Przedmiot badania: Selektor jakości gaze przy zmianie telefonu i warunków. Kandydatura, bez zatwierdzonego odrębnego protokołu.

- **Główny wynik proponowany:** Nieokreślony w rejestrze. Wymaga zdefiniowania metryki, estymandu i jednostki analizy przed rozpoczęciem badania.
- **Odrębność naukowa:** Należy porównać źródłowy protokół z pokrewnymi manuskryptami przed formalizacją hipotezy.
- **Uzasadnienie klasyfikacji:** WŁĄCZYĆ do P01; niezależny AI-paper tylko po nowej metodzie i held-out walidacji. [Klasyfikacja portfolio 2026-11-20] Obecnie ocena ważności/kalibracji jakości pomiaru gaze w ramach P01; zachować IDEA_HOLD. Tylko nowa, przenoszalna metoda selective prediction z walidacją na nowych urządzeniach mogłaby w przyszłości uzasadnić osobną pracę ARC AI.
- **Powiązane rekordy:** `MSC-EYE-P01` (arc-mobile-eyetracking:P01)

## Stanowisko badawcze

**Wstępne powiązanie:** `ST-02`. To propozycja na podstawie domeny, a nie potwierdzenie uruchomienia aparatury.

[Stanowiska ARC](https://github.com/MatPomGit/research-autopilot/blob/main/docs/portfolio/reorganizacja-systemu-badan/shared_research_platforms.md); [inwentarz prywatny `devices`](https://github.com/MatPomGit/devices).

## Powiązane aplikacje APP

- `app-eye-mobile` (`APP-ARC-04`), `PRIMARY`, profil `android-native`, bramka `MVP`.

## Powiązane biblioteki LIB

- `lib-events`: planowana zależność pośrednia przez `app-eye-mobile`; brak dowodu integracji.
- `lib-eye`: planowana zależność pośrednia przez `app-eye-mobile`; brak dowodu integracji.
- `lib-image` (historyczna nazwa; wymaga uzgodnienia z `lib-vis`): planowana zależność pośrednia przez `app-eye-mobile`; brak dowodu integracji.

Relacje APP i LIB pochodzą odpowiednio z `app_publication_links.csv` i `component_dependencies.csv`. Są kandydaturami, nie dowodami wykonania prac. Aktualność nazw `lib-signals`, `lib-image` i `lib-llm` wymaga osobnego uzgodnienia z nowymi repozytoriami.

## Proweniencja, metodologia i bramki

- **UID źródłowy:** `arc-mobile-eyetracking:F-GAZE-01`; repozytorium `MatPomGit/arc-mobile-eyetracking`, identyfikator `F-GAZE-01`.
- **Ścieżka źródłowa:** `manuscripts/FUTURE_RESEARCH_PROPOSALS.md`.
- **Materiał:** [źródło projektu](https://github.com/MatPomGit/arc-mobile-eyetracking/blob/main/manuscripts/FUTURE_RESEARCH_PROPOSALS.md).
- **Rejestr MSC:** [kanoniczna macierz](https://github.com/MatPomGit/research-autopilot/blob/main/docs/portfolio/reorganizacja-systemu-badan/publication_matrix.csv).

Przed badaniem wymagane są niezależny wynik i plan analizy, źródła literaturowe, ocena nowości, kontrola praw do danych/oprogramowania, ocena bezpieczeństwa i kwalifikacja etyczna, jeżeli dotyczy. Szkic nie zawiera danych empirycznych ani nie potwierdza dostępności stanowiska.
