# MSC-PAIN-P07 | Eksperymentalne odróżnianie motywów ponoszenia osobistego kosztu

**Właściciel naukowy i autor szkicu:** Mateusz Pomianek. Obszar: social. Rodzaj: IDEA. Stan: PROSPECTIVE, wersja 1.0.0 (26.11.2026).

Katalog zawiera [manuskrypt](main.tex), [kartę badania](study.md), [projekt prerejestracji OSF](preregistration.md), [słownik danych](data-dictionary.csv), [przegląd źródeł i czasopism](evidence.md) oraz [syntetyczne wyniki symulacji](analysis/power.csv). Dane empiryczne nie zostały zebrane.

## Odtwarzanie symulacji i PDF

Uruchom z tego katalogu w Pythonie 3.12 i środowisku z TeX Live, TikZ, BibTeX, natbib oraz obsługą języka polskiego.

    python -m pip install -r analysis/requirements.txt
    OPENBLAS_NUM_THREADS=1 python -m unittest discover -s analysis -v
    OPENBLAS_NUM_THREADS=1 python analysis/power.py --output analysis/power.csv --repetitions 300
    python analysis/summarize.py
    latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex

CSV obejmuje 30 kombinacji scenariusza i liczebności. Odtworzenie nie wymaga danych uczestników. Przed uruchomieniem badania potrzebne są potwierdzenie wykonalności, decyzja etyczna oraz zamrożenie protokołu.

## Wyniki kontroli wersji 1.0.0

Symulacja wykonana w Pythonie 3.12.14, NumPy 2.3.5 i SciPy 1.17.0. Ziarno 20261126, 300 replikacji na kombinację, 9000 łącznie. Scenariusz zerowy dał 1,7–3,3% dodatnich rozstrzygnięć przy nominalnej jednostronnej części błędu 2,5%. Odnotowano jedno nieudane dopasowanie, w scenariuszu zerowym dla N=320. Scenariusz heterogeniczny generuje losowe nachylenie kosztu, którego roboczy model z losowym wyrazem wolnym nie zawiera. Powstałe oszacowanie mocy dotyczy zachowania procedury przy tej niezgodności. Mechanizm rezygnacji jest losowy i obejmuje całą sesję, a braki informacyjne obejmuje plan analizy wrażliwości dla badania właściwego.

Sprawdzono cztery testy regresyjne symulacji, dwa testy spójności katalogu ARC oraz kompilację LaTeX z BibTeX. Przejrzano sześć stron PDF, w tym dwa rysunki TikZ, tabelę mocy i bibliografię. Lokalna kompilacja użyła stylu natbib abbrvnat. Ostateczne formatowanie należy dostosować do wybranego czasopisma.
