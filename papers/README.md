# Katalogi artykułów ARC Neuro

Struktura obejmuje **63 źródła manuskryptów LaTeX** w pięciu obszarach badawczych. Każdy katalog `slot-NNN` zawiera samodzielny plik `main.tex`, będący pierwszym szkicem naukowym (v0.1.0). Teksty nie przedstawiają niezweryfikowanych wyników ani bibliografii.

| Obszar | Katalog | Liczba |
| --- | --- | ---: |
| Neurorozwój i neuroróżnorodność | [ndd](ndd/README.md) | 16 |
| Afekt i regulacja emocji | [affect](affect/README.md) | 4 |
| Poznanie i interakcja człowiek–AI | [cognition](cognition/README.md) | 13 |
| Relacje i zachowania społeczne | [social](social/README.md) | 22 |
| Psychometria i metody pomiarowe | [psychometrics](psychometrics/README.md) | 8 |

Oznaczenia `slot-NNN` są numerami porządkowymi miejsc w strukturze, a nie identyfikatorami publikacji. Publiczne informacje o pracach są udostępniane po weryfikacji ich statusu i praw do rozpowszechniania.

[Wykaz zatwierdzonych projektów](../docs/projects.md).

## Kompilacja

W wybranym katalogu wykonać `pdflatex -halt-on-error -interaction=nonstopmode main.tex`. Wymagany jest TeX z obsługą języka polskiego. Pliki PDF i pomocnicze powstające podczas składu nie są źródłem manuskryptu.
