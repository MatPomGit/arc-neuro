# Wydania i migawki ARC Neuro

Wydanie repozytorium programu nie jest wydaniem manuskryptu ani zgłoszeniem artykułu. `VERSION` i `CHANGELOG.md` opisują wersję standardu, struktury i narzędzi. Identyfikator wydania powinien być jednoznaczny i zawierać SemVer, datę oraz tag wskazujący konkretny commit SHA. Wydanie nie promuje automatycznie żadnego `paper.status`, `PROJECT_STATE.yaml.phase` lub `public_listing`.

## Bramka przed wydaniem

Sprawdź `main`, rzeczywiste PR/review i warunki ruleset, wszystkie testy na exact SHA, brak danych prywatnych w historii nowych zmian, poprawność katalogu i brak niezatwierdzonych plików `pages/`. Upewnij się, że katalog jest zgodny z `publication-approvals.json`, a nowa wersja nie zawiera ujawnionych ID urządzeń, danych uczestników i prywatnych mapowań `papers/`.

Opublikowanie tagu lub GitHub Release wymaga oddzielnego zatwierdzenia właściciela. Wpis o wydaniu nie oznacza zbudowania strony Pages, publikacji danych, poprawności naukowej ani wysłania manuskryptu. Nie włączaj automatycznego wydania po scaleniu PR.

Zapisz źródłowy SHA, zakres, testy, zmiany kompatybilności, decyzję właściciela i ewentualny plan wycofania. Nie twórz ponownie numeracji prac w osobnym changelogu.
