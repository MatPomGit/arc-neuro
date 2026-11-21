# MSC-AAL-P06 — plan badania i powiązania

**Temat:** Autonomia użytkownika, zaufanie i obciążenie opiekuna przy eskalacji alarmów AAL

**Program:** `arc-neuro`. **Obszar:** `autonomy-social-hci`. **Typ:** `IDEA` (CANDIDATE). **Stan źródła:** `NEW_UNVERIFIED_IDEA`. **Tryb integracji:** `INDEX_ONLY_NO_NEW_FOLDER`.

## Cel, wynik główny i granice badania

Przedmiot badania: Autonomia użytkownika, zaufanie i obciążenie opiekuna przy eskalacji alarmów AAL. Kandydatura, bez zatwierdzonego odrębnego protokołu.

- **Główny wynik proponowany:** Nieokreślony w rejestrze. Wymaga zdefiniowania metryki, estymandu i jednostki analizy przed rozpoczęciem badania.
- **Odrębność naukowa:** Należy porównać źródłowy protokół z pokrewnymi manuskryptami przed formalizacją hipotezy.
- **Uzasadnienie klasyfikacji:** Nowa propozycja z 2026-11-20. Wpływ polityki informowania i zgody na postrzeganą autonomię, zaufanie i zmęczenie alarmami; nie powiela ergonomii UI P02 ani detekcji P03. Pierwsze eksperymenty scenariuszowe, bez uruchamiania rzeczywistych alarmów i bez niezatwierdzonych badań grup wrażliwych.
- **Powiązane rekordy:** `MSC-AAL-P02` (carehome-aal:AAL-P02), `MSC-AAL-P03` (carehome-aal:AAL-P03)

## Stanowisko badawcze

**Wstępne powiązanie:** `ST-06`. To propozycja na podstawie domeny, a nie potwierdzenie uruchomienia aparatury.

[Stanowiska ARC](https://github.com/MatPomGit/research-autopilot/blob/main/docs/portfolio/reorganizacja-systemu-badan/shared_research_platforms.md); [inwentarz prywatny `devices`](https://github.com/MatPomGit/devices).

## Powiązane aplikacje APP

- `app-study-web` (`APP-ARC-06`), `OPTIONAL`, profil `web-study`, bramka `RESEARCH_GO`.
- `app-carehome` (`APP-ARC-09`), `OPTIONAL`, profil `aal-simulator`, bramka `RESEARCH_GO`.

## Powiązane biblioteki LIB

- `lib-adapt`: planowana zależność pośrednia przez `app-carehome`; brak dowodu integracji.
- `lib-events`: planowana zależność pośrednia przez `app-study-web`, `app-carehome`; brak dowodu integracji.
- `lib-llm` (historyczna nazwa; wymaga uzgodnienia z `lib-vlm`): planowana zależność pośrednia przez `app-study-web`, `app-carehome`; brak dowodu integracji.
- `lib-sim`: planowana zależność pośrednia przez `app-carehome`; brak dowodu integracji.
- `lib-study`: planowana zależność pośrednia przez `app-study-web`; brak dowodu integracji.
- `lib-vlm`: planowana zależność pośrednia przez `app-carehome`; brak dowodu integracji.

Relacje APP i LIB pochodzą odpowiednio z `app_publication_links.csv` i `component_dependencies.csv`. Są kandydaturami, nie dowodami wykonania prac. Aktualność nazw `lib-signals`, `lib-image` i `lib-llm` wymaga osobnego uzgodnienia z nowymi repozytoriami.

## Proweniencja, metodologia i bramki

- **UID źródłowy:** `carehome-aal:AAL-P06`; repozytorium `MatPomGit/research-autopilot`, identyfikator `AAL-P06`.
- **Ścieżka źródłowa:** `docs/portfolio/reorganizacja-systemu-badan/carehome_aal_concept.md`.
- **Materiał:** [źródło projektu](https://github.com/MatPomGit/research-autopilot/blob/24600e13ffd23c5ac25e7d9e288341ad4b8c5114/docs/portfolio/reorganizacja-systemu-badan/carehome_aal_concept.md).
- **Rejestr MSC:** [kanoniczna macierz](https://github.com/MatPomGit/research-autopilot/blob/main/docs/portfolio/reorganizacja-systemu-badan/publication_matrix.csv).

Przed badaniem wymagane są niezależny wynik i plan analizy, źródła literaturowe, ocena nowości, kontrola praw do danych/oprogramowania, ocena bezpieczeństwa i kwalifikacja etyczna, jeżeli dotyczy. Szkic nie zawiera danych empirycznych ani nie potwierdza dostępności stanowiska.
