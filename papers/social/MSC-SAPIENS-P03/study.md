# MSC-SAPIENS-P03 — plan badania i powiązania

**Temat:** Odbiór zachowania humanoida na nagraniu wideo

**Program:** `arc-neuro`. **Obszar:** `social`. **Typ:** `IDEA` (CANDIDATE). **Stan źródła:** `IDEA_HOLD`. **Tryb integracji:** `INDEX_ONLY_NO_NEW_FOLDER`.

## Cel, wynik główny i granice badania

Przedmiot badania: Odbiór zachowania humanoida na nagraniu wideo. Kandydatura, bez zatwierdzonego odrębnego protokołu.

- **Główny wynik proponowany:** Nieokreślony w rejestrze. Wymaga zdefiniowania metryki, estymandu i jednostki analizy przed rozpoczęciem badania.
- **Odrębność naukowa:** Należy porównać źródłowy protokół z pokrewnymi manuskryptami przed formalizacją hipotezy.
- **Uzasadnienie klasyfikacji:** Wstępne badanie kontrolne; z zasady NIE nowy artykuł.
- **Powiązane rekordy:** `MSC-SAPIENS-P01` (arc-sapiens:P01)

## Stanowisko badawcze

**Wstępne powiązanie:** `ST-04`. To propozycja na podstawie domeny, a nie potwierdzenie uruchomienia aparatury.

[Stanowiska ARC](https://github.com/MatPomGit/research-autopilot/blob/main/docs/portfolio/reorganizacja-systemu-badan/shared_research_platforms.md); [inwentarz prywatny `devices`](https://github.com/MatPomGit/devices).

## Powiązane aplikacje APP

- `app-2d-desktop` (`APP-ARC-01D`), `OPTIONAL`, profil `desktop-browser`, bramka `RESEARCH_GO`.
- `app-study-web` (`APP-ARC-06`), `OPTIONAL`, profil `web-study`, bramka `RESEARCH_GO`.

## Powiązane biblioteki LIB

- `lib-events`: planowana zależność pośrednia przez `app-2d-desktop`, `app-study-web`; brak dowodu integracji.
- `lib-eye`: planowana zależność pośrednia przez `app-2d-desktop`; brak dowodu integracji.
- `lib-image` (historyczna nazwa; wymaga uzgodnienia z `lib-vis`): planowana zależność pośrednia przez `app-2d-desktop`; brak dowodu integracji.
- `lib-llm` (historyczna nazwa; wymaga uzgodnienia z `lib-vlm`): planowana zależność pośrednia przez `app-study-web`; brak dowodu integracji.
- `lib-study`: planowana zależność pośrednia przez `app-2d-desktop`, `app-study-web`; brak dowodu integracji.

Relacje APP i LIB pochodzą odpowiednio z `app_publication_links.csv` i `component_dependencies.csv`. Są kandydaturami, nie dowodami wykonania prac. Aktualność nazw `lib-signals`, `lib-image` i `lib-llm` wymaga osobnego uzgodnienia z nowymi repozytoriami.

## Proweniencja, metodologia i bramki

- **UID źródłowy:** `arc-sapiens:F-SAPIENS-02`; repozytorium `MatPomGit/arc-sapiens`, identyfikator `F-SAPIENS-02`.
- **Ścieżka źródłowa:** `manuscripts/FUTURE_RESEARCH_PROPOSALS.md`.
- **Materiał:** [źródło projektu](https://github.com/MatPomGit/arc-sapiens/blob/main/manuscripts/FUTURE_RESEARCH_PROPOSALS.md).
- **Rejestr MSC:** [kanoniczna macierz](https://github.com/MatPomGit/research-autopilot/blob/main/docs/portfolio/reorganizacja-systemu-badan/publication_matrix.csv).

Przed badaniem wymagane są niezależny wynik i plan analizy, źródła literaturowe, ocena nowości, kontrola praw do danych/oprogramowania, ocena bezpieczeństwa i kwalifikacja etyczna, jeżeli dotyczy. Szkic nie zawiera danych empirycznych ani nie potwierdza dostępności stanowiska.
