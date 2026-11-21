# Polityka GitHub Pages ARC Neuro

**Jedynym dopuszczonym źródłem przyszłej publicznej strony jest `pages/`**, z `mkdocs.yml` wskazującym `docs_dir: pages`. `docs/`, `papers/`, `portfolio/`, `equipment/`, `.github/` i inne zasoby repo nie mogą być bezpośrednio publikowane. Dotyczy to także sytuacji, gdy repozytorium źródłowe jest prywatne: GitHub Pages może mieć inną widoczność.

`config/pages-policy.json` jest jawną listą dozwolonych plików i zatwierdzonych zasobów motywu. `scripts/validate_pages.py` kontroluje niezatwierdzone pliki, linki do materiałów wewnętrznych, redakcyjne komentarze, instrukcje agentów, próbki sekretów, symlinki i wybrane metadane obrazów. Każde rozszerzenie listy wymaga recenzji. Status `PASS` walidatora **nie potwierdza** opublikowania ani poufności strony.

Generator `scripts/build_public_catalog.py` zapisuje publiczną listę do **`pages/projects.md`**, wyłącznie z zatwierdzonych publicznie projektów. Nie zapisuje do `docs/projects.md`. Źródłem praw do publikacji są rzeczywiste recenzje właściciela i `portfolio/publication-approvals.json`; sama flaga `public_listing` nie jest zgodą.

Przed oddzielnym wdrożeniem sprawdź wynikowe HTML, źródła, linki, prawa do zdjęć, metadane i rzeczywiste ustawienia widoczności. Nie wybieraj w ustawieniach GitHub Pages źródła `main:/docs`, `main:/` ani całego repo. Publikację przeprowadza wyłącznie ręcznie wywołany `.github/workflows/pages-publish.yml`, po sprawdzeniu gałęzi `main` i ustawieniu `publication_authorized=true`. Każde uruchomienie waliduje źródło i wynikowy HTML, po czym przekazuje do GitHub Pages wyłącznie `site/`. Nie ma automatycznego publikowania po scaleniu PR. Jeśli źródło Pages w ustawieniach repozytorium nie jest ustawione na **GitHub Actions**, wdrożenie musi zostać uprzednio skonfigurowane przez administratora.

Na publicznej stronie nie umieszczaj instrukcji dla agentów, poleceń edytorskich, procedur współtworzenia repozytorium, danych uczestników, identyfikatorów prywatnej aparatury ani mapowań neutralnych slotów 63 publikacji.

## Repozytorium źródłowe a publikacja strony

Repozytorium `MatPomGit/arc-neuro` jest **publiczne**: pliki `papers/`, ich tytuły i treść oraz historia commitów są dostępne bez uruchamiania Pages. Ograniczenie `docs_dir: pages` chroni jedynie wejście generatora strony, **nie ogranicza dostępu do kodu ani wcześniejszych commitów**. W PR #8 znajdują się szkice 63 prac; przed scaleniem właściciel musi odrębnie ocenić ich publiczną treść. Brak wpisów w `portfolio/publication-approvals.json` oznacza brak akceptacji publicznego katalogu, a nie techniczną poufność źródeł. Usunięcie pliku z kolejnego commitu nie usuwa go automatycznie z historii. W razie ujawnienia danych wrażliwych stosować procedurę incydentową.
