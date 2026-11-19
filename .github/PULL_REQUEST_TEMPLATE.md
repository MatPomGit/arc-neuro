## Zakres i powód

- Program / linia badawcza:
- Kanoniczne repozytoria, których dotyczy PR:
- Czy zmienia właściciela manuskryptu? (tak/nie)
- Czy ujawnia wpis publicznie? (tak/nie)

## Weryfikacja

- [ ] Sprawdzono aktualne remote HEAD/SHA i pochodzenie danych.
- [ ] Wykonano `python scripts/validate_repository.py --phase scaffold`.
- [ ] Wykonano `python -m unittest discover -s tests -v`.
- [ ] Potwierdzono brak prywatnych odnośników w publicznych docs.
- [ ] Wpisano ograniczenia, recenzję i plan wycofania.

## Zatwierdzenie publicznych metadanych (gdy `public_listing=true`)

- [ ] Właściciel rzeczywiście przejrzał dokładny wpis projektu, jego URL i uprawnienia publikacyjne.
- [ ] Rejestr `portfolio/publication-approvals.json` wskazuje istniejącą recenzję GitHub i SHA-256 niezmienionego wpisu.
- [ ] Zweryfikowano autora i treść wskazanej recenzji w GitHub; poprawność URL w CI nie stanowi dowodu zgody.
