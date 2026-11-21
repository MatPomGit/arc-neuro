# ADR-0002: granica publikacji ARC Neuro

**Data:** 2026-11-20  
**Status:** proposed

## Kontekst

W repo znajdują się polityki, stan programu, notatki i katalogi manuskryptów nazwane identyfikatorami MSC; pełny eksport `docs/` mógłby ujawnić treści przeznaczone do pracy wewnętrznej. Metadane źródłowe i flagi publiczności nie są równoznaczne ze zgodą właściciela.

## Decyzja proponowana

Publiczne Pages otrzymuje tylko jawnie zatwierdzone pliki z `pages/`, a `pages/projects.md` jest deterministycznie generowany wyłącznie z poprawnie zatwierdzonych publicznych projektów. Każdy zasób przechodzi walidację allowlisty i recenzję wynikowego HTML. Nie wdrażamy automatycznego publikowania strony wraz z merge.

## Alternatywy i skutki

Publikowanie `docs/` jest łatwiejsze, ale łamie zasadę minimalnej ekspozycji. Osobna projekcja publiczna wymaga dodatkowego kroku synchronizacji generatora i ręcznej kontroli, za to chroni rejestry i teksty robocze.
