# ARC Neuro

**Program naukowy:** `arc-neuro` | **Właściciel naukowy:** Mateusz Pomianek | **Status:** publiczny katalog programu w przygotowaniu.

ARC Neuro porządkuje badania nad poznaniem, afektem, zachowaniem, neurorozwojem, psychofizjologią i psychometrią. Kryterium przynależności projektu stanowi jego główna hipoteza i wkład dotyczący funkcjonowania człowieka, a nie samo użycie EEG, eye trackingu, AI lub XR.

## Linie badawcze

- **NDD:** neurorozwój i neuroróżnorodność.
- **Affect:** emocje, stres i regulacja.
- **Cognition:** uwaga, pamięć i interakcja człowiek-AI.
- **Social:** przywiązanie i zachowania społeczne.
- **Psychometrics:** konstrukcja i walidacja narzędzi pomiarowych.

Identyfikatory i pełne nazwy określa [`areas/index.json`](areas/index.json). Nie tworzymy osobnego `arc-ndd`; NDD jest linią ARC Neuro.

## Propozycje nowych badań

Przed zatwierdzeniem manuskryptów rozpatrywany jest [pomysł MSC-AAL-P08: pamięć prospektywna w zadaniach domowych](docs/research-proposals-2026.md). To hipoteza do oceny i przygotowania eksperymentu, **nie wpis w publicznym katalogu zatwierdzonych artykułów**.

## Katalogi robocze artykułów

W katalogu [`papers/`](papers/README.md) znajduje się **63 roboczych manuskryptów LaTeX** w pięciu liniach badawczych, w katalogach nazwanych kanonicznymi identyfikatorami MSC i rzeczywistymi tytułami. Każda praca ma własny plik `main.tex` (wersja 0.1.1) z odrębnym tytułem i roboczym zarysem naukowym. **Repozytorium jest publiczne, zatem widoczne są również źródła tych szkiców**, niezależnie od przyszłej strony Pages. Pliki nie są ukończonymi publikacjami: wymagają jeszcze weryfikacji literatury, procedur oraz wyników.

## Rejestr badań i otwarta nauka

Rejestry [projektów](portfolio/projects.json), [artykułów](portfolio/papers.json) i [zależności](portfolio/dependencies.json) zawierają wyłącznie informacje indywidualnie zatwierdzone do publicznego indeksowania. Aktualnie pozostają puste; nie oznacza to braku prowadzonych badań.

Każdy samodzielny projekt zachowuje kanoniczny protokół, manuskrypty i dowody w swoim repozytorium. ARC nie kopiuje surowych danych uczestników ani kodu aplikacji. Projekty dopuszczone do otwartej nauki będą prezentowane na indywidualnych witrynach GitHub Pages, a ARC zapewni publiczny katalog odnośników. **Publikacja strony ARC nie jest jeszcze skonfigurowana.**

## Kontrole lokalne

```bash
python scripts/validate_repository.py --phase scaffold
python -m unittest discover -s tests -v
python scripts/build_public_catalog.py
# W CI: rzeczywisty smoke test kompilacji 63 źródeł PDF i build MkDocs
```

Stan bieżący projektu i historyczna migawka służą różnym celom. Testy publicznego indeksu nie wymagają dostępu do niepublicznych projektów ani danych.

Zobacz [zakres programu](docs/scientific-scope.md), [zasady publikacji](docs/publication-policy.md), [politykę danych](docs/data-policy.md) i [reprodukowalność](REPRODUCIBILITY.md).

Powiązane zadanie: [#1](https://github.com/MatPomGit/arc-neuro/issues/1).

## Licencja

Autorski kod i związana z nim dokumentacja tego repozytorium są udostępniane na licencji [MIT](LICENSE) (© 2026 Mateusz Pomianek). Przy ponownym wykorzystaniu zachowaj informację o prawach autorskich i treść licencji.

Licencja nie obejmuje automatycznie zasobów zewnętrznych, połączonych repozytoriów, artykułów naukowych, danych uczestników ani materiałów osób trzecich. Takie zasoby podlegają odrębnym warunkom i zgodom. Publiczna dostępność informacji nie jest równoznaczna z prawem do ich dalszego wykorzystania.

Plik `PROJECT_STATE.yaml` jest automatycznie sprawdzany pod względem zgodności właściciela, wersji, liczb projektów i artykułów oraz konfiguracji publikacji z rejestrami JSON. Dopuszczony format to prosty, jawny podzbiór YAML: pola skalarne i lista `known_blockers`, bez zagnieżdżonych obiektów.

Publiczny katalog wymaga osobnej decyzji publikacyjnej w `portfolio/publication-approvals.json` z SHA-256 dokładnych metadanych i odnośnikiem do recenzji właściciela. Sama flaga `public_listing=true` nie wystarcza do publikacji. CI weryfikuje zgodność techniczną, ale nie zastępuje rzeczywistej recenzji GitHub.


## Architektura i proces badawczy

Program zarządza metadanymi przez [ARCHITECTURE.md](ARCHITECTURE.md), [GOVERNANCE.md](GOVERNANCE.md), [SECURITY.md](SECURITY.md) i [ADR](docs/adr/README.md). Zasady przyjmowania prac określa [standard Issues](docs/issues.md): jedno sprawdzalne zadanie, typ intencji, klasyfikacja `agent-work-classification:v1`, zależności i dowody exact SHA. Formularze obejmują zadania, usterki, programy badań i przygotowanie manuskryptu.

Publiczna projekcja programu jest przygotowywana w [`pages/`](pages/index.md), a zatwierdzony katalog projektów w [`pages/projects.md`](pages/projects.md). `docs/` pozostaje dokumentacją techniczną; wydania i GitHub Pages mają odrębne bramki [publikacyjne](docs/pages.md).
