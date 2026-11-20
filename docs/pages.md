# Polityka GitHub Pages ARC Neuro

**Jedynym dopuszczonym źródłem przyszłej publicznej strony jest `pages/`**, z `mkdocs.yml` wskazującym `docs_dir: pages`. `docs/`, `papers/`, `portfolio/`, `equipment/`, `.github/` i inne zasoby repo nie mogą być bezpośrednio publikowane. Dotyczy to także sytuacji, gdy repozytorium źródłowe jest prywatne: GitHub Pages może mieć inną widoczność.

`config/pages-policy.json` jest jawną listą dozwolonych plików i zatwierdzonych zasobów motywu. `scripts/validate_pages.py` kontroluje niezatwierdzone pliki, linki do materiałów wewnętrznych, redakcyjne komentarze, instrukcje agentów, próbki sekretów, symlinki i wybrane metadane obrazów. Każde rozszerzenie listy wymaga recenzji. Status `PASS` walidatora **nie potwierdza** opublikowania ani poufności strony.

Generator `scripts/build_public_catalog.py` zapisuje publiczną listę do **`pages/projects.md`**, wyłącznie z zatwierdzonych publicznie projektów. Nie zapisuje do `docs/projects.md`. Źródłem praw do publikacji są rzeczywiste recenzje właściciela i `portfolio/publication-approvals.json`; sama flaga `public_listing` nie jest zgodą.

Przed oddzielnym wdrożeniem sprawdź wynikowe HTML, źródła, linki, prawa do zdjęć, metadane i rzeczywiste ustawienia widoczności. Nie wybieraj w ustawieniach GitHub Pages źródła `main:/docs`, `main:/` ani całego repo. W tym repo nie dodano workflow automatycznego publikowania z merge.

Na publicznej stronie nie umieszczaj instrukcji dla agentów, poleceń edytorskich, procedur współtworzenia repozytorium, danych uczestników, identyfikatorów prywatnej aparatury ani mapowań neutralnych slotów 63 publikacji.
