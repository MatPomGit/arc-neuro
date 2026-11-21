# MSC-EYE-P03 — plan badania i powiązania

**Temat:** Zgodność klasyfikacji regionów spojrzenia w mobilnej grze 2D przy zmianie warunków

**Program:** `arc-neuro`. **Obszar:** `mobile-gaze-metrology`. **Typ:** `IDEA` (CANDIDATE). **Stan źródła:** `IDEA_DEFINED`. **Tryb integracji:** `INDEX_ONLY_NO_NEW_FOLDER`.

## Cel, wynik główny i granice badania

Przedmiot badania: Zgodność klasyfikacji regionów spojrzenia w mobilnej grze 2D przy zmianie warunków. Kandydatura, bez zatwierdzonego odrębnego protokołu.

- **Główny wynik proponowany:** F1/zgodność klasyfikacji ROI w scenariuszach gry i zmiennych warunkach
- **Odrębność naukowa:** Metoda funkcjonalna ROI i brak przełączeń błędnych podczas gry; osobny outcome od punktowego błędu urządzenia P01.
- **Uzasadnienie klasyfikacji:** Gra 2D w przeglądarce, bez gogli VR i bez EEG. Możliwy overlap z kwalifikacją mobilnej okulografii; nie przypisywać automatycznie XR. [Klasyfikacja portfolio 2026-11-20] Wkład główny to trafność regionowego pomiaru spojrzenia u człowieka na smartfonie w grze 2D, bez XR. Możliwy zakres wspólny z arc-mobile-eyetracking:P01; utrzymać odrębny wpis źródłowy bez zakładania drugiego manuskryptu do audytu nowości. AUDYT DUPLIKACJI: wysokie ryzyko ponownego sformułowania artykułu metodycznego arc-mobile-eyetracking:P01; eksperyment ROI w grze 2D może być częścią tej walidacji. | Proponowane doprecyzowanie zakresu portfolio 2026-11-20, wymaga zatwierdz
- **Powiązane rekordy:** `MSC-EYE-P01` (arc-mobile-eyetracking:P01)

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

- **UID źródłowy:** `arc-xr:GAZE-METHOD`; repozytorium `MatPomGit/arc-xr`, identyfikator `GAZE-METHOD`.
- **Ścieżka źródłowa:** `docs/pomysl_badawczy_mobile_gaze_adaptive.md`.
- **Materiał:** [źródło projektu](https://github.com/MatPomGit/arc-xr/blob/main/docs/pomysl_badawczy_mobile_gaze_adaptive.md).
- **Rejestr MSC:** [kanoniczna macierz](https://github.com/MatPomGit/research-autopilot/blob/main/docs/portfolio/reorganizacja-systemu-badan/publication_matrix.csv).

Przed badaniem wymagane są niezależny wynik i plan analizy, źródła literaturowe, ocena nowości, kontrola praw do danych/oprogramowania, ocena bezpieczeństwa i kwalifikacja etyczna, jeżeli dotyczy. Szkic nie zawiera danych empirycznych ani nie potwierdza dostępności stanowiska.
