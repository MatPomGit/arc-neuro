# MSC-TRUST-P01 — plan badania i powiązania

**Temat:** Kalibracja polegania na wskazówkach AI w ekranie 2D, XR i symulowanym humanoidzie

**Program:** `arc-neuro`. **Obszar:** `trust-agency-cross-media`. **Typ:** `IDEA` (CANDIDATE). **Stan źródła:** `NEW_CROSS_DOMAIN_IDEA_HOLD`. **Tryb integracji:** `INDEX_ONLY_NO_NEW_FOLDER`.

## Cel, wynik główny i granice badania

Przedmiot badania: Kalibracja polegania na wskazówkach AI w ekranie 2D, XR i symulowanym humanoidzie. Kandydatura, bez zatwierdzonego odrębnego protokołu.

- **Główny wynik proponowany:** Nieokreślony w rejestrze. Wymaga zdefiniowania metryki, estymandu i jednostki analizy przed rozpoczęciem badania.
- **Odrębność naukowa:** Należy porównać źródłowy protokół z pokrewnymi manuskryptami przed formalizacją hipotezy.
- **Uzasadnienie klasyfikacji:** Nowy warunkowy eksperyment z odpowiednim poleganiem na rekomendacjach i wpływem medium oraz wyjaśnienia abstencji. Nie powielać zaufania AAL P06/HRI M08 ani efektu perswazji CR P01; osobna hipoteza interakcyjna, zdefiniowany ground truth, etyka przed danymi ludzi.
- **Powiązane rekordy:** `MSC-CR-P01` (arc-ai-cognitive-resilience:P01), `MSC-AAL-P06` (carehome-aal:AAL-P06), `MSC-AR-P18` (arc-xr:XR-IDEA-12), `MSC-HRI-P08` (arc-hri-safety:M08)

## Stanowisko badawcze

**Wstępne powiązanie:** `ST-07`. To propozycja na podstawie domeny, a nie potwierdzenie uruchomienia aparatury.

[Stanowiska ARC](https://github.com/MatPomGit/research-autopilot/blob/main/docs/portfolio/reorganizacja-systemu-badan/shared_research_platforms.md); [inwentarz prywatny `devices`](https://github.com/MatPomGit/devices).

## Powiązane aplikacje APP

- `app-2d-desktop` (`APP-ARC-01D`), `COMPARATOR`, profil `desktop-browser`, bramka `RESEARCH_GO`.
- `app-study-web` (`APP-ARC-06`), `OPTIONAL`, profil `web-study`, bramka `RESEARCH_GO`.
- `app-xr` (`APP-ARC-07`), `OPTIONAL`, profil `unity-openxr`, bramka `RESEARCH_GO`.
- `app-hri-console` (`APP-ARC-08`), `OPTIONAL`, profil `ros2-replay`, bramka `RESEARCH_GO`.
- `app-carehome` (`APP-ARC-09`), `OPTIONAL`, profil `aal-simulator`, bramka `RESEARCH_GO`.

## Powiązane biblioteki LIB

- `lib-adapt`: planowana zależność pośrednia przez `app-carehome`; brak dowodu integracji.
- `lib-asr`: planowana zależność pośrednia przez `app-xr`, `app-hri-console`; brak dowodu integracji.
- `lib-audio`: planowana zależność pośrednia przez `app-hri-console`; brak dowodu integracji.
- `lib-events`: planowana zależność pośrednia przez `app-2d-desktop`, `app-study-web`, `app-xr`, `app-hri-console`, `app-carehome`; brak dowodu integracji.
- `lib-eye`: planowana zależność pośrednia przez `app-2d-desktop`; brak dowodu integracji.
- `lib-image` (historyczna nazwa; wymaga uzgodnienia z `lib-vis`): planowana zależność pośrednia przez `app-2d-desktop`, `app-xr`, `app-hri-console`; brak dowodu integracji.
- `lib-llm` (historyczna nazwa; wymaga uzgodnienia z `lib-vlm`): planowana zależność pośrednia przez `app-study-web`, `app-carehome`; brak dowodu integracji.
- `lib-ros`: planowana zależność pośrednia przez `app-hri-console`; brak dowodu integracji.
- `lib-sim`: planowana zależność pośrednia przez `app-hri-console`, `app-carehome`; brak dowodu integracji.
- `lib-study`: planowana zależność pośrednia przez `app-2d-desktop`, `app-study-web`; brak dowodu integracji.
- `lib-unity`: planowana zależność pośrednia przez `app-xr`; brak dowodu integracji.
- `lib-vlm`: planowana zależność pośrednia przez `app-xr`, `app-hri-console`, `app-carehome`; brak dowodu integracji.
- `lib-voice`: planowana zależność pośrednia przez `app-xr`; brak dowodu integracji.
- `OptiCore`: planowana zależność pośrednia przez `app-xr`; brak dowodu integracji.

Relacje APP i LIB pochodzą odpowiednio z `app_publication_links.csv` i `component_dependencies.csv`. Są kandydaturami, nie dowodami wykonania prac. Aktualność nazw `lib-signals`, `lib-image` i `lib-llm` wymaga osobnego uzgodnienia z nowymi repozytoriami.

## Proweniencja, metodologia i bramki

- **UID źródłowy:** `cross-arc:CROSS-ARC-03`; repozytorium `MatPomGit/research-autopilot`, identyfikator `CROSS-ARC-03`.
- **Ścieżka źródłowa:** `docs/portfolio/reorganizacja-systemu-badan/shared_research_platforms.md`.
- **Materiał:** [źródło projektu](https://github.com/MatPomGit/research-autopilot/blob/c397169d8630090f38bacf091947cc47083f006c/docs/portfolio/reorganizacja-systemu-badan/shared_research_platforms.md).
- **Rejestr MSC:** [kanoniczna macierz](https://github.com/MatPomGit/research-autopilot/blob/main/docs/portfolio/reorganizacja-systemu-badan/publication_matrix.csv).

Przed badaniem wymagane są niezależny wynik i plan analizy, źródła literaturowe, ocena nowości, kontrola praw do danych/oprogramowania, ocena bezpieczeństwa i kwalifikacja etyczna, jeżeli dotyczy. Szkic nie zawiera danych empirycznych ani nie potwierdza dostępności stanowiska.
