# MSC-AAL-P02 — plan badania i powiązania

**Temat:** Redukcja obciążenia poznawczego dzięki kontekstowej adaptacji interfejsu Smart Home

**Program:** `arc-neuro`. **Obszar:** `cognition-accessibility-hci`. **Typ:** `IDEA` (CANDIDATE). **Stan źródła:** `SOURCE_PLANNED_ARTICLE`. **Tryb integracji:** `INDEX_ONLY_NO_NEW_FOLDER`.

## Cel, wynik główny i granice badania

Przedmiot badania: Redukcja obciążenia poznawczego dzięki kontekstowej adaptacji interfejsu Smart Home. Kandydatura, bez zatwierdzonego odrębnego protokołu.

- **Główny wynik proponowany:** Nieokreślony w rejestrze. Wymaga zdefiniowania metryki, estymandu i jednostki analizy przed rozpoczęciem badania.
- **Odrębność naukowa:** Należy porównać źródłowy protokół z pokrewnymi manuskryptami przed formalizacją hipotezy.
- **Uzasadnienie klasyfikacji:** Tytuł źródłowy: Reducing Cognitive Load in Smart Home Control: Evaluation of a Context-Aware Adaptive User Interface for Users with Cognitive and Motor Impairments. Wyniki: błędy, czas, kroki, NASA-TLX, SUS; Tobii Eye Tracker 5 wyłącznie w kompatybilnej geometrii pomiarowej; próba 20–30 osób wyłącznie wstępne założenie, nie analiza mocy.
- **Powiązane rekordy:** Nie zarejestrowano.

## Stanowisko badawcze

**Wstępne powiązanie:** `ST-06`. To propozycja na podstawie domeny, a nie potwierdzenie uruchomienia aparatury.

[Stanowiska ARC](https://github.com/MatPomGit/research-autopilot/blob/main/docs/portfolio/reorganizacja-systemu-badan/shared_research_platforms.md); [inwentarz prywatny `devices`](https://github.com/MatPomGit/devices).

## Powiązane aplikacje APP

- `app-carehome` (`APP-ARC-09`), `PRIMARY`, profil `aal-simulator`, bramka `MVP`.

## Powiązane biblioteki LIB

- `lib-adapt`: planowana zależność pośrednia przez `app-carehome`; brak dowodu integracji.
- `lib-events`: planowana zależność pośrednia przez `app-carehome`; brak dowodu integracji.
- `lib-llm` (historyczna nazwa; wymaga uzgodnienia z `lib-vlm`): planowana zależność pośrednia przez `app-carehome`; brak dowodu integracji.
- `lib-sim`: planowana zależność pośrednia przez `app-carehome`; brak dowodu integracji.
- `lib-vlm`: planowana zależność pośrednia przez `app-carehome`; brak dowodu integracji.

Relacje APP i LIB pochodzą odpowiednio z `app_publication_links.csv` i `component_dependencies.csv`. Są kandydaturami, nie dowodami wykonania prac. Aktualność nazw `lib-signals`, `lib-image` i `lib-llm` wymaga osobnego uzgodnienia z nowymi repozytoriami.

## Proweniencja, metodologia i bramki

- **UID źródłowy:** `carehome-aal:AAL-P02`; repozytorium `MatPomGit/research-autopilot`, identyfikator `AAL-P02`.
- **Ścieżka źródłowa:** `docs/portfolio/reorganizacja-systemu-badan/carehome_aal_concept.md`.
- **Materiał:** [źródło projektu](https://github.com/MatPomGit/research-autopilot/blob/24600e13ffd23c5ac25e7d9e288341ad4b8c5114/docs/portfolio/reorganizacja-systemu-badan/carehome_aal_concept.md).
- **Rejestr MSC:** [kanoniczna macierz](https://github.com/MatPomGit/research-autopilot/blob/main/docs/portfolio/reorganizacja-systemu-badan/publication_matrix.csv).

Przed badaniem wymagane są niezależny wynik i plan analizy, źródła literaturowe, ocena nowości, kontrola praw do danych/oprogramowania, ocena bezpieczeństwa i kwalifikacja etyczna, jeżeli dotyczy. Szkic nie zawiera danych empirycznych ani nie potwierdza dostępności stanowiska.
