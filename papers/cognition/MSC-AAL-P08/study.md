# MSC-AAL-P08 — plan badania i powiązania

**Temat:** Pamięć prospektywna po przerwaniu zadania: przypomnienia kontekstowe wobec czasowych

**Program:** `arc-neuro`. **Obszar:** `prospective-memory-interruptions-aal`. **Typ:** `IDEA` (CANDIDATE). **Stan źródła:** `NEW_CROSS_PROGRAM_IDEA_HOLD`. **Tryb integracji:** `INDEX_ONLY_NO_NEW_FOLDER`.

## Cel, wynik główny i granice badania

Przedmiot badania: Pamięć prospektywna po przerwaniu zadania: przypomnienia kontekstowe wobec czasowych. Kandydatura, bez zatwierdzonego odrębnego protokołu.

- **Główny wynik proponowany:** Nieokreślony w rejestrze. Wymaga zdefiniowania metryki, estymandu i jednostki analizy przed rozpoczęciem badania.
- **Odrębność naukowa:** Należy porównać źródłowy protokół z pokrewnymi manuskryptami przed formalizacją hipotezy.
- **Uzasadnienie klasyfikacji:** [Nowa propozycja burzy mózgów 2026-11-20, priorytet B] Nowa hipoteza o realizacji odroczonej intencji, nie o ogólnej ergonomii AAL ani czasie recovery z gry ADHD. Prosty wirtualny dom 2D, losowana sekwencja, primary omission error; test na zdrowych dorosłych dopiero po etyce; nie wnioskować o MCI/demencji. Wkład i nowość niezatwierdzone; nie tworzyć manuskryptu przed audytem. Propozycja znajduje się w dokumentacji programu, w otwartym PR, bez wpisu do katalogu zatwierdzonych publikacji.
- **Powiązane rekordy:** `MSC-AAL-P02` (carehome-aal:AAL-P02), `MSC-ADHD-P01` (arc-adhd-game:P01), `MSC-AAL-P06` (carehome-aal:AAL-P06)

## Stanowisko badawcze

**Wstępne powiązanie:** `ST-07`. To propozycja na podstawie domeny, a nie potwierdzenie uruchomienia aparatury.

[Stanowiska ARC](https://github.com/MatPomGit/research-autopilot/blob/main/docs/portfolio/reorganizacja-systemu-badan/shared_research_platforms.md); [inwentarz prywatny `devices`](https://github.com/MatPomGit/devices).

## Powiązane aplikacje APP

- `app-2d-desktop` (`APP-ARC-01D`), `PRIMARY`, profil `desktop-browser`, bramka `RESEARCH_GO`.
- `app-carehome` (`APP-ARC-09`), `OPTIONAL`, profil `aal-simulator`, bramka `RESEARCH_GO`.

## Powiązane biblioteki LIB

- `lib-adapt`: planowana zależność pośrednia przez `app-carehome`; brak dowodu integracji.
- `lib-events`: planowana zależność pośrednia przez `app-2d-desktop`, `app-carehome`; brak dowodu integracji.
- `lib-eye`: planowana zależność pośrednia przez `app-2d-desktop`; brak dowodu integracji.
- `lib-image` (historyczna nazwa; wymaga uzgodnienia z `lib-vis`): planowana zależność pośrednia przez `app-2d-desktop`; brak dowodu integracji.
- `lib-llm` (historyczna nazwa; wymaga uzgodnienia z `lib-vlm`): planowana zależność pośrednia przez `app-carehome`; brak dowodu integracji.
- `lib-sim`: planowana zależność pośrednia przez `app-carehome`; brak dowodu integracji.
- `lib-study`: planowana zależność pośrednia przez `app-2d-desktop`; brak dowodu integracji.
- `lib-vlm`: planowana zależność pośrednia przez `app-carehome`; brak dowodu integracji.

Relacje APP i LIB pochodzą odpowiednio z `app_publication_links.csv` i `component_dependencies.csv`. Są kandydaturami, nie dowodami wykonania prac. Aktualność nazw `lib-signals`, `lib-image` i `lib-llm` wymaga osobnego uzgodnienia z nowymi repozytoriami.

## Proweniencja, metodologia i bramki

- **UID źródłowy:** `arc-neuro:NEURO-IDEA-01`; repozytorium `MatPomGit/arc-neuro`, identyfikator `NEURO-IDEA-01`.
- **Ścieżka źródłowa:** `docs/research-proposals-2026.md`.
- **Materiał:** [źródło projektu](https://github.com/MatPomGit/arc-neuro/blob/da575fccc2dff1acb2af9937f0e1c56a28718051/docs/research-proposals-2026.md).
- **Rejestr MSC:** [kanoniczna macierz](https://github.com/MatPomGit/research-autopilot/blob/main/docs/portfolio/reorganizacja-systemu-badan/publication_matrix.csv).

Przed badaniem wymagane są niezależny wynik i plan analizy, źródła literaturowe, ocena nowości, kontrola praw do danych/oprogramowania, ocena bezpieczeństwa i kwalifikacja etyczna, jeżeli dotyczy. Szkic nie zawiera danych empirycznych ani nie potwierdza dostępności stanowiska.
