# MSC-DERA-P01 — plan badania i powiązania

**Temat:** Struktura czynnikowa i trafność narzędzia DERA-HRI do oceny doświadczenia interakcji z humanoidem

**Program:** `arc-neuro`. **Obszar:** `dera-hri-psychometrics`. **Typ:** `IDEA` (CANDIDATE). **Stan źródła:** `CANDIDATE_VALIDATION_DATA_REQUIRED`. **Tryb integracji:** `INDEX_ONLY_NO_NEW_FOLDER`.

## Cel, wynik główny i granice badania

Przedmiot badania: Struktura czynnikowa i trafność narzędzia DERA-HRI do oceny doświadczenia interakcji z humanoidem. Kandydatura, bez zatwierdzonego odrębnego protokołu.

- **Główny wynik proponowany:** Replikowalność modelu czynnikowego DERA-HRI na niezależnej próbie oraz przedziały dla rzetelności i trafności
- **Odrębność naukowa:** Psychometryczna walidacja skali, odrębna od zależności między subiektywnym i fizycznym bezpieczeństwem w MSC-HRI-P08.
- **Uzasadnienie klasyfikacji:** Kandydacki artykuł naukowy oparty na istniejącym artefakcie INS-DERA-I01. Brak danych empirycznych i dowodów samodzielnego efektu; przed samodzielnym czasopiśmiennym manuskryptem konieczne GO, zgodność źródłowego protokołu, prawa i etyka.
- **Powiązane rekordy:** `INS-DERA-I01` (arc-dera-hri:CANDIDATE), `MSC-HRI-P08` (arc-hri-safety:M08)

## Stanowisko badawcze

**Wstępne powiązanie:** `ST-04`, `ST-07`. To propozycja na podstawie domeny, a nie potwierdzenie uruchomienia aparatury.

[Stanowiska ARC](https://github.com/MatPomGit/research-autopilot/blob/main/docs/portfolio/reorganizacja-systemu-badan/shared_research_platforms.md); [inwentarz prywatny `devices`](https://github.com/MatPomGit/devices).

## Powiązane aplikacje APP

- `app-study-web` (`APP-ARC-06`), `OPTIONAL`, profil `web-study`, bramka `RESEARCH_GO`.
- `app-hri-console` (`APP-ARC-08`), `OPTIONAL`, profil `ros2-replay`, bramka `RESEARCH_GO`.

## Powiązane biblioteki LIB

- `lib-asr`: planowana zależność pośrednia przez `app-hri-console`; brak dowodu integracji.
- `lib-audio`: planowana zależność pośrednia przez `app-hri-console`; brak dowodu integracji.
- `lib-events`: planowana zależność pośrednia przez `app-study-web`, `app-hri-console`; brak dowodu integracji.
- `lib-image` (historyczna nazwa; wymaga uzgodnienia z `lib-vis`): planowana zależność pośrednia przez `app-hri-console`; brak dowodu integracji.
- `lib-llm` (historyczna nazwa; wymaga uzgodnienia z `lib-vlm`): planowana zależność pośrednia przez `app-study-web`; brak dowodu integracji.
- `lib-ros`: planowana zależność pośrednia przez `app-hri-console`; brak dowodu integracji.
- `lib-sim`: planowana zależność pośrednia przez `app-hri-console`; brak dowodu integracji.
- `lib-study`: planowana zależność pośrednia przez `app-study-web`; brak dowodu integracji.
- `lib-vlm`: planowana zależność pośrednia przez `app-hri-console`; brak dowodu integracji.

Relacje APP i LIB pochodzą odpowiednio z `app_publication_links.csv` i `component_dependencies.csv`. Są kandydaturami, nie dowodami wykonania prac. Aktualność nazw `lib-signals`, `lib-image` i `lib-llm` wymaga osobnego uzgodnienia z nowymi repozytoriami.

## Proweniencja, metodologia i bramki

- **UID źródłowy:** `portfolio:MSC-DERA-P01`; repozytorium `MatPomGit/research-autopilot`, identyfikator `MSC-DERA-P01`.
- **Ścieżka źródłowa:** `docs/portfolio/reorganizacja-systemu-badan/manuscript_plans/MSC-DERA-P01.md`.
- **Materiał:** [źródło projektu](https://github.com/MatPomGit/research-autopilot/blob/be4b5d4d4dcee1770777cdf42e0a80783c630d25/docs/portfolio/reorganizacja-systemu-badan/manuscript_plans/MSC-DERA-P01.md).
- **Rejestr MSC:** [kanoniczna macierz](https://github.com/MatPomGit/research-autopilot/blob/main/docs/portfolio/reorganizacja-systemu-badan/publication_matrix.csv).

Przed badaniem wymagane są niezależny wynik i plan analizy, źródła literaturowe, ocena nowości, kontrola praw do danych/oprogramowania, ocena bezpieczeństwa i kwalifikacja etyczna, jeżeli dotyczy. Szkic nie zawiera danych empirycznych ani nie potwierdza dostępności stanowiska.
