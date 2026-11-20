# Katalogi artykułów ARC Neuro

Struktura obejmuje **63 źródła manuskryptów LaTeX** w pięciu obszarach badawczych. Każdy katalog `slot-NNN` zawiera samodzielny plik `main.tex`, będący pierwszym szkicem naukowym (v0.1.0). Teksty nie przedstawiają niezweryfikowanych wyników ani bibliografii.

| Obszar | Katalog | Liczba |
| --- | --- | ---: |
| Neurorozwój i neuroróżnorodność | [ndd](ndd/README.md) | 16 |
| Afekt i regulacja emocji | [affect](affect/README.md) | 4 |
| Poznanie i interakcja człowiek–AI | [cognition](cognition/README.md) | 13 |
| Relacje i zachowania społeczne | [social](social/README.md) | 22 |
| Psychometria i metody pomiarowe | [psychometrics](psychometrics/README.md) | 8 |

**Uwaga o jawności:** repozytorium ARC Neuro jest publiczne. Tytuły i treści wszystkich 63 plików `main.tex` są widoczne w kodzie i historii Git, niezależnie od ograniczeń GitHub Pages. Są to szkice koncepcyjne, a nie zatwierdzone protokoły, artykuły ani rekordy katalogu. Zatwierdzenie ich jawności jako materiałów źródłowych i zatwierdzenie wpisów publikacyjnych są odrębnymi decyzjami. Nie umieszczaj w nich danych uczestników ani mapowań na niepubliczne projekty.\n\nOznaczenia `slot-NNN` są numerami porządkowymi miejsc w strukturze, a nie identyfikatorami publikacji. Publiczne informacje o pracach są udostępniane po weryfikacji ich statusu i praw do rozpowszechniania.

[Wykaz zatwierdzonych projektów](../pages/projects.md).

## Kompilacja

W wybranym katalogu wykonać `pdflatex -halt-on-error -interaction=nonstopmode main.tex`. Wymagany jest TeX z obsługą języka polskiego. Pliki PDF i pomocnicze powstające podczas składu nie są źródłem manuskryptu.
