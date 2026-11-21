# MSC-EYE-P01 — plan badania i powiązania

**Temat:** Trafność punktowego pomiaru spojrzenia z kamery Android: kalibracja i powtarzalność

**Program:** `arc-neuro`. **Obszar:** `gaze-measurement-validity`. **Typ:** `MANUSCRIPT` (MANUSCRIPT). **Stan źródła:** `PLANNED`. **Tryb integracji:** `LINK_ONLY`.

## Cel, wynik główny i granice badania

Przedmiot badania: Trafność punktowego pomiaru spojrzenia z kamery Android: kalibracja i powtarzalność. Istnieje ślad źródłowego manuskryptu; stan dowodów wymaga weryfikacji.

- **Główny wynik proponowany:** Błąd punktowy w pikselach/kącie oraz powtarzalność na sesjach testowych
- **Odrębność naukowa:** Metrologiczna dokładność/precision estymacji punktu; nie klasyfikacja regionów w grze.
- **Uzasadnienie klasyfikacji:** [Klasyfikacja portfolio 2026-11-20] Wkład główny: trafność, precyzja, powtarzalność i granice mobilnego pomiaru zachowań wzrokowych u człowieka. Algorytm estymacji jest narzędziem, nie udokumentowaną nową metodą ML. AUDYT DUPLIKACJI: wysokie podobieństwo artykułu metodycznego z arc-xr:GAZE-METHOD; należy wyznaczyć jeden kanoniczny tor walidacji Android gaze. | Proponowane doprecyzowanie zakresu portfolio 2026-11-20, wymaga zatwierdzenia naukowego: Metrologiczna dokładność/precision estymacji punktu; nie klasyfikacja regionów w grze. Główny wynik do prerejestracji: Błąd punktowy w pikselach/kącie oraz powtarzalność na sesjach testowych. Tytuł 
- **Powiązane rekordy:** `MSC-EYE-P03` (arc-xr:GAZE-METHOD)

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

- **UID źródłowy:** `arc-mobile-eyetracking:P01`; repozytorium `MatPomGit/arc-mobile-eyetracking`, identyfikator `P01`.
- **Ścieżka źródłowa:** `manuscript/README.md`.
- **Materiał:** [źródło projektu](https://github.com/MatPomGit/arc-mobile-eyetracking/blob/main/manuscript/README.md).
- **Rejestr MSC:** [kanoniczna macierz](https://github.com/MatPomGit/research-autopilot/blob/main/docs/portfolio/reorganizacja-systemu-badan/publication_matrix.csv).

Przed badaniem wymagane są niezależny wynik i plan analizy, źródła literaturowe, ocena nowości, kontrola praw do danych/oprogramowania, ocena bezpieczeństwa i kwalifikacja etyczna, jeżeli dotyczy. Szkic nie zawiera danych empirycznych ani nie potwierdza dostępności stanowiska.
