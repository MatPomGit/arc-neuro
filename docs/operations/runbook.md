# Procedura utrzymania ARC Neuro

**Stan:** publiczne repozytorium katalogowe, puste zatwierdzone rejestry i nieuruchomione Pages. Dozwolone kontrole offline nie wymagają prywatnych projektów.

## Przed zmianą

Odczytaj Issues, PR, dokładny `main` i HEAD, aktualny WIP, `PROJECT_STATE.yaml`, `portfolio/*.json` oraz [stan ochrony gałęzi](https://github.com/MatPomGit/arc-neuro/issues/7). Sprawdź, czy planowany wpis jest publiczny i rzeczywiście zatwierdzony.

## Weryfikacja offline

```bash
python scripts/validate_repository.py --phase scaffold
python scripts/validate_documentation.py
python scripts/validate_pages.py
python scripts/validate_issues.py
python -m unittest discover -s tests -v
python scripts/build_public_catalog.py
git diff --exit-code -- pages/projects.md
```

CI działa na przypiętym SHA PR oraz syntetycznej rewizji scalającej, bez sekretów. Wyniki kontroli źródeł nie potwierdzają skuteczności metod, rzeczywistej recenzji właściciela ani poprawności aktualnego ustawienia ruleset.

## Publikacja

Nie publikuj `docs/` lub całego repo. Tylko `pages/` może wejść do źródła Pages po walidacji allowlisty, sprawdzeniu wygenerowanego HTML, odnośników, licencji i rzeczywistej zgody na dane oraz oddzielnym zatwierdzeniu wdrożenia. Nie twórz automatycznego deploy.

## Odbiór

Dla każdego PR zapisz komendy i wyniki `PASS/FAIL/NOT_RUN/UNAVAILABLE`, finalny SHA, recenzenta, zgodę lub blokadę i kolejny bezpieczny krok. Po merge ponownie odczytaj `main`; nie usuwaj cudzych gałęzi, worktree ani historycznych rejestrów.
