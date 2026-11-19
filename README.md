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

## Rejestr badań i otwarta nauka

Rejestry [projektów](portfolio/projects.json), [artykułów](portfolio/papers.json) i [zależności](portfolio/dependencies.json) zawierają wyłącznie informacje indywidualnie zatwierdzone do publicznego indeksowania. Aktualnie pozostają puste; nie oznacza to braku prowadzonych badań.

Każdy samodzielny projekt zachowuje kanoniczny protokół, manuskrypty i dowody w swoim repozytorium. ARC nie kopiuje surowych danych uczestników ani kodu aplikacji. Projekty dopuszczone do otwartej nauki będą prezentowane na indywidualnych witrynach GitHub Pages, a ARC zapewni publiczny katalog odnośników. **Publikacja strony ARC nie jest jeszcze skonfigurowana.**

## Kontrole lokalne

```bash
python scripts/validate_repository.py --phase scaffold
python -m unittest discover -s tests -v
python scripts/build_public_catalog.py
```

Stan bieżący projektu i historyczna migawka służą różnym celom. Testy publicznego indeksu nie wymagają dostępu do niepublicznych projektów ani danych.

Zobacz [zakres programu](docs/scientific-scope.md), [zasady publikacji](docs/publication-policy.md), [politykę danych](docs/data-policy.md) i [reprodukowalność](REPRODUCIBILITY.md).

Powiązane zadanie: [#1](https://github.com/MatPomGit/arc-neuro/issues/1).
