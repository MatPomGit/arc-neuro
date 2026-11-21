# MSC-ADHD-P05 — plan badania i powiązania

**Temat:** EEG Muse S Athena zsynchronizowane ze zdarzeniami regulacji

**Program:** `arc-neuro`. **Obszar:** `ndd`. **Typ:** `MANUSCRIPT` (MANUSCRIPT). **Stan źródła:** `ACTIVE`. **Tryb integracji:** `LINK_ONLY`.

## Cel, wynik główny i granice badania

Przedmiot badania: EEG Muse S Athena zsynchronizowane ze zdarzeniami regulacji. Istnieje ślad źródłowego manuskryptu; stan dowodów wymaga weryfikacji.

- **Główny wynik proponowany:** Nieokreślony w rejestrze. Wymaga zdefiniowania metryki, estymandu i jednostki analizy przed rozpoczęciem badania.
- **Odrębność naukowa:** Należy porównać źródłowy protokół z pokrewnymi manuskryptami przed formalizacją hipotezy.
- **Uzasadnienie klasyfikacji:** Klasyfikacja wg pytania badawczego: EEG jest sygnałem fizjologicznym do zbadania mechanizmu regulacji i czasowej zgodności z zadaniem; pomiar nie jest jeszcze kwalifikowany. Status źródła: ACTIVE. Nie oznacza zatwierdzonych danych ani gotowości publikacji.
- **Powiązane rekordy:** Nie zarejestrowano.

## Stanowisko badawcze

**Wstępne powiązanie:** `ST-01`. To propozycja na podstawie domeny, a nie potwierdzenie uruchomienia aparatury.

[Stanowiska ARC](https://github.com/MatPomGit/research-autopilot/blob/main/docs/portfolio/reorganizacja-systemu-badan/shared_research_platforms.md); [inwentarz prywatny `devices`](https://github.com/MatPomGit/devices).

## Powiązane aplikacje APP

- `app-regulation-mobile` (`APP-ARC-02`), `PRIMARY`, profil `android-native`, bramka `SOURCE_VALIDATION`.
- `app-eeg-neurolyze` (`APP-ARC-03`), `SIGNAL_SOURCE`, profil `python-eeg`, bramka `DEVICE_RIGHTS`.

## Powiązane biblioteki LIB

- `lib-adapt`: planowana zależność pośrednia przez `app-regulation-mobile`; brak dowodu integracji.
- `lib-events`: planowana zależność pośrednia przez `app-regulation-mobile`, `app-eeg-neurolyze`; brak dowodu integracji.
- `lib-signals` (historyczna nazwa; wymaga uzgodnienia z `lib-sig`): planowana zależność pośrednia przez `app-eeg-neurolyze`; brak dowodu integracji.
- `lib-sim`: planowana zależność pośrednia przez `app-eeg-neurolyze`; brak dowodu integracji.

Relacje APP i LIB pochodzą odpowiednio z `app_publication_links.csv` i `component_dependencies.csv`. Są kandydaturami, nie dowodami wykonania prac. Aktualność nazw `lib-signals`, `lib-image` i `lib-llm` wymaga osobnego uzgodnienia z nowymi repozytoriami.

## Proweniencja, metodologia i bramki

- **UID źródłowy:** `arc-adhd-game:P05`; repozytorium `MatPomGit/arc-adhd-game`, identyfikator `P05`.
- **Ścieżka źródłowa:** `manuscripts/05-eeg-muse-athena/README.md`.
- **Materiał:** [źródło projektu](https://github.com/MatPomGit/arc-adhd-game/blob/main/manuscripts/05-eeg-muse-athena/README.md).
- **Rejestr MSC:** [kanoniczna macierz](https://github.com/MatPomGit/research-autopilot/blob/main/docs/portfolio/reorganizacja-systemu-badan/publication_matrix.csv).

Przed badaniem wymagane są niezależny wynik i plan analizy, źródła literaturowe, ocena nowości, kontrola praw do danych/oprogramowania, ocena bezpieczeństwa i kwalifikacja etyczna, jeżeli dotyczy. Szkic nie zawiera danych empirycznych ani nie potwierdza dostępności stanowiska.
