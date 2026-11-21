# MSC-EYE-P04 — plan badania i powiązania

**Temat:** Kiedy adaptacyjny interfejs powinien podpowiadać? Ostrożna adaptacja 2D oparta na jakości spojrzenia

**Program:** `arc-neuro`. **Obszar:** `cognition`. **Typ:** `IDEA` (CANDIDATE). **Stan źródła:** `IDEA_DEFINED`. **Tryb integracji:** `INDEX_ONLY_NO_NEW_FOLDER`.

## Cel, wynik główny i granice badania

Przedmiot badania: Kiedy adaptacyjny interfejs powinien podpowiadać? Ostrożna adaptacja 2D oparta na jakości spojrzenia. Kandydatura, bez zatwierdzonego odrębnego protokołu.

- **Główny wynik proponowany:** Nieokreślony w rejestrze. Wymaga zdefiniowania metryki, estymandu i jednostki analizy przed rozpoczęciem badania.
- **Odrębność naukowa:** Należy porównać źródłowy protokół z pokrewnymi manuskryptami przed formalizacją hipotezy.
- **Uzasadnienie klasyfikacji:** Wynik główny: liczba zbędnych interwencji i zachowanie użytkownika w mobilnej grze 2D. Nie XR.
- **Powiązane rekordy:** `MSC-EYE-P03` (arc-xr:GAZE-METHOD), `MSC-AFFECT-P06` (arc-affective:P06)

## Stanowisko badawcze

**Wstępne powiązanie:** `ST-02`. To propozycja na podstawie domeny, a nie potwierdzenie uruchomienia aparatury.

[Stanowiska ARC](https://github.com/MatPomGit/research-autopilot/blob/main/docs/portfolio/reorganizacja-systemu-badan/shared_research_platforms.md); [inwentarz prywatny `devices`](https://github.com/MatPomGit/devices).

## Powiązane aplikacje APP

- `app-2d-mobile` (`APP-ARC-01M`), `PRIMARY`, profil `mobile-browser`, bramka `MVP`.
- `app-eye-mobile` (`APP-ARC-04`), `SIGNAL_SOURCE`, profil `android-native`, bramka `CROSS_PLATFORM`.
- `app-eye-desktop` (`APP-ARC-05`), `COMPARATOR`, profil `desktop-webcam`, bramka `CROSS_PLATFORM`.

## Powiązane biblioteki LIB

- `lib-adapt`: planowana zależność pośrednia przez `app-2d-mobile`; brak dowodu integracji.
- `lib-events`: planowana zależność pośrednia przez `app-2d-mobile`, `app-eye-mobile`, `app-eye-desktop`; brak dowodu integracji.
- `lib-eye`: planowana zależność pośrednia przez `app-2d-mobile`, `app-eye-mobile`, `app-eye-desktop`; brak dowodu integracji.
- `lib-image` (historyczna nazwa; wymaga uzgodnienia z `lib-vis`): planowana zależność pośrednia przez `app-2d-mobile`, `app-eye-mobile`, `app-eye-desktop`; brak dowodu integracji.
- `lib-study`: planowana zależność pośrednia przez `app-2d-mobile`; brak dowodu integracji.

Relacje APP i LIB pochodzą odpowiednio z `app_publication_links.csv` i `component_dependencies.csv`. Są kandydaturami, nie dowodami wykonania prac. Aktualność nazw `lib-signals`, `lib-image` i `lib-llm` wymaga osobnego uzgodnienia z nowymi repozytoriami.

## Proweniencja, metodologia i bramki

- **UID źródłowy:** `arc-xr:GAZE-EXPERIMENT`; repozytorium `MatPomGit/arc-xr`, identyfikator `GAZE-EXPERIMENT`.
- **Ścieżka źródłowa:** `docs/pomysl_badawczy_mobile_gaze_adaptive.md`.
- **Materiał:** [źródło projektu](https://github.com/MatPomGit/arc-xr/blob/main/docs/pomysl_badawczy_mobile_gaze_adaptive.md).
- **Rejestr MSC:** [kanoniczna macierz](https://github.com/MatPomGit/research-autopilot/blob/main/docs/portfolio/reorganizacja-systemu-badan/publication_matrix.csv).

Przed badaniem wymagane są niezależny wynik i plan analizy, źródła literaturowe, ocena nowości, kontrola praw do danych/oprogramowania, ocena bezpieczeństwa i kwalifikacja etyczna, jeżeli dotyczy. Szkic nie zawiera danych empirycznych ani nie potwierdza dostępności stanowiska.
