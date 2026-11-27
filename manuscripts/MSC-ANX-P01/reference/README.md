# Referencyjny model obliczeniowy MSC-ANX-P01

Właściciel naukowy: Mateusz Pomianek. Status: prospektywny model syntetyczny, nie aplikacja do zbierania danych. Kod jest publiczną ilustracją kontraktu i nie zastępuje przyszłego kanonicznego repozytorium badania.

- design.py: deterministyczny manifest 240 prób klasyfikacji (48 bazowych, 192 mieszane), 94 switch / 94 repeat, cztery nieokreślone pierwsze przejścia, 96 wyborów. Dokładnie 12 powtórzeń identycznego bodźca w każdym warunku. Marginesy są kontrolowane w całej sesji; generator przyjmuje wyłącznie sekwencje spełniające jawne tolerancje i przerywa po 128 nieudanych próbach. Wersja bodźców 0.4.2, wersja protokołu 0.4.0. Tolerancje są wstępnymi progami inżynieryjnymi, nie gwarantują pełnej ortogonalności ani rzetelności psychometrycznej. Ziarna 0–31 ilustrują 32 kombinacje przypisania odpowiedzi, kolejności bloków bazowych, zadań i domen decyzji; w badaniu alokację trzeba równoważyć niezależnie od identyfikatora.
- audit_design.py: audyt 2048 kolejnych ziaren, zakresy marginesów i raport JSON; niezerowy kod wyjścia przy niepowodzeniu.
- synthetic.py: generowanie wyłącznie rekordów SYN, obliczanie median kosztu i bazowego RT, trafności i kwalifikacji. Minimum 24 poprawne bazowe próby jest dodatkowym proponowanym progiem. Timeout jest niepowodzeniem w analizie trafności, nigdy ważną poprawną reakcją. Nie przechowuje danych ani nie wysyła żądań sieciowych.
- statistical.py: H1 OLS z HC3 i dwustronnym wnioskowaniem t, kompletne przypadki, jawne kodowanie kategorii i warianty bez bazowego RT oraz depresyjności. H2/H3: uzupełniające GEE logit z odporną macierzą kowariancji klastrowaną po osobie i korektą Holma. GEE nie jest konfirmacyjnym GLMM; różne estymandy marginalne i warunkowe. Dane wejściowe wyłącznie syntetyczne. Stałe współzmienne są jawnie pomijane, stały predyktor hipotezy lub niedostateczny rząd macierzy przerywają analizę.
- power.py: analityczne przybliżenie Fishera i symulacja Monte Carlo zmiennej liczebności po niezależnej utracie; nie symuluje jeszcze rzetelności kosztu ani modeli H2/H3. Założenie r dotyczy korelacji częściowej obserwowanych zmiennych, nie efektu latentnego.

Uruchomienie z katalogu repozytorium:

```sh
python3 -B -m unittest discover -s tests -p test_anx_reference.py -v
python3 -B papers/cognition/MSC-ANX-P01/reference/audit_design.py --count 2048
python3 -B papers/cognition/MSC-ANX-P01/reference/power.py --recruited 444 --r .15 --repetitions 5000 --seed 42
```

Kolejne prace: niezależna weryfikacja generatora, symulacja niezależnych parametrów poziomu prób, walidacja modeli HC3 i GLMM oraz analiza rzetelności. Implementacja przeglądarkowa, zatwierdzone skale i akwizycja danych wymagają osobnego kanonicznego środowiska, testów timing i decyzji etycznej. Nie wdrażać na GitHub Pages.

## Opcjonalna warstwa statystyczna

```sh
python3 -m venv .venv-anx
.venv-anx/bin/python -m pip install -r papers/cognition/MSC-ANX-P01/reference/requirements-ci.txt
.venv-anx/bin/python -m unittest discover -s papers/cognition/MSC-ANX-P01/reference -p test_statistical.py -v
.venv-anx/bin/python papers/cognition/MSC-ANX-P01/reference/statistical.py --n 80 --seed 42
```

Bez utrwalania danych, tylko raport syntetyczny. requirements-ci.txt przypina wersje zależności bezpośrednich i przechodnich odczytane z CI #45837988941 (Ubuntu x86_64, Python 3.12.3). Jest to lock wersji, nie hash-lock artefaktów; pozostałe platformy wymagają weryfikacji. requirements-analysis.txt zachowuje minimalną listę bibliotek do analizy. Modele GLMM oraz analiza prób RT: mixed_models.py. Weryfikacja poprawności implementacji nie zastępuje walidacji modelu na zatwierdzonym protokole.

## Modele mieszane (P3.3b)

- H2/H3: częstotliwościowy logistyczny model z losowym interceptem uczestnika, maksymalizacja scałkowanego likelihood za pomocą kwadratury Gaussa–Hermite'a (32/64 węzły; kontrola 96), obserwowana informacja i przedziały Walda, Holm. Współczynnik warunkowy, nie marginalny GEE.
- RT: model liniowy mieszany na log(RT), interakcja switch × GAD-7/5, losowy intercept i nachylenie switch. Wariant wyłącznie z interceptem wymaga jawnego wyboru. Nie zastępuje głównego H1 w ms.
- Trafność: logistyczny model z losowym interceptem i interakcją. Timeout pozostaje błędem, próby technicznie nieważne wykluczane; selekcja prób na podstawie poprawności dotyczy tylko RT. Modele prób mają odrębne kryteria od głównego H1; nie zawierają bazowego RT.
- Odrzucenie modeli na granicy wariancji, bez zbieżności lub dostatecznej dokładności kwadratury. Generator syntetyczny z P3.1 nie zawiera osobniczych efektów losowych wyboru ani trafności, więc jego pełny raport GLMM może zostać prawidłowo odrzucony. Testy odzyskiwania parametrów wykorzystują osobne dane z zadanym efektem losowym. Nie ma jeszcze pełnego badania kalibracji, pokrycia CI ani symulacji mocy.

```sh
.venv-anx/bin/python -m unittest discover -s papers/cognition/MSC-ANX-P01/reference -p 'test_mixed_models.py' -v
```

## Symulacja mocy H2/H3 (P3.4)

choice_power.py wykorzystuje referencyjny GLMM, wspólnych uczestników i współzmienne oraz skorelowane losowe intercepty obu zadań. W scenariuszu domyślnym: 444 rekrutowanych, 20% niezależnej utraty uczestników, 2% niezależnej utraty prób, 48 prób/zadanie, beta warunkowa na 5 punktów GAD-7: -0,15 i -0,20; SD interceptów 0,65, korelacja 0,4. Są to założenia projektowe, nie oszacowania z pilotażu. Raport obejmuje odrzucenia surowe i po Holmie, moc kierunkową, moc dowolnej i wszystkich alternatyw, FWER przy co najmniej jednej prawdziwej H0, pokrycie CI, bias i nieudane dopasowania. Niepowodzenia mają p=1 w rodzinie Holma i pozostają w mianowniku mocy; pokrycie warunkowe raportowane osobno.

Przykład uruchomienia pojedynczego scenariusza (koszt CPU zależy od liczby powtórzeń):

```sh
.venv-anx/bin/python papers/cognition/MSC-ANX-P01/reference/choice_power.py --recruited 444 --repetitions 100 --seed 42
```

Plan właściwej kalibracji przed zamrożeniem: n=250/350/444/550, beta=0/-0,10/-0,15/-0,20 (w tym częściowe H0), SD=0,35/0,65/1,0, rho=0/0,4/0,8; nie wykonywać pełnego iloczynu bez budżetu CPU. Najpierw scenariusze bazowe i skrajne, następnie zawężenie. Minimum 2000 replikacji na finalny scenariusz, ocena MC CI i stopy nieudanych dopasowań; dla FWER użyć także obu H0. Domyślne 100 replikacji jest próbą rozpoznawczą, nie podstawą decyzji o liczebności. Testy CI obejmują kontrakt symulatora, nie wykonują pełnej kampanii obliczeniowej. Nie uruchamiać kampanii na płatnej infrastrukturze bez zgody.

## Rzetelność i tłumienie efektu (P3.5)

reliability.py: losowy, odtwarzalny podział zaplanowanych prób w stratach blok × typ przejścia, przed filtracją poprawności i RT. Każda połowa ma 47 przejść switch i 47 repeat; minimum 25 poprawnych prób każdego rodzaju na połowę, dodatkowo kwalifikacja H1. Koszt w każdej połowie jest różnicą median. Korelacja Pearsona między kosztami i korekta Spearmana–Browna; bootstrap percentylowy po uczestnikach (pary zachowane, podział ustalony). Raportuje się liczbę wykluczeń, ważnych replikacji, różnicę średnich i SD kosztów połówek. Ujemny wynik nie jest zerowany; przy r=-1 korekta nieokreślona. SB zakłada równoległość połówek; nie jest testem trafności ani stabilności czasowej. Przed pilotażem ustalić próg rzetelności i procedurę modyfikacji zadania; powtórzyć analizę z różnymi podziałami oraz test-retest w osobnej sesji. 

Analiza tłumienia efektu: r_obserwowane = r_latentne × sqrt(Rx × Ry), przy klasycznym niezależnym błędzie pomiarowym zmiennych po residualizacji. Nie stosować automatycznie do korelacji częściowych z błędem współzmiennych; r=0,15 z H1 oznacza dotychczas efekt obserwowany, scenariusz latentny jest odrębną analizą wrażliwości. Nie zastępuje symulacji na poziomie prób.

```sh
.venv-anx/bin/python papers/cognition/MSC-ANX-P01/reference/reliability.py --n 80 --bootstrap 2000
.venv-anx/bin/python -m unittest discover -s papers/cognition/MSC-ANX-P01/reference -p 'test_reliability.py' -v
```

## Demonstrator

[Instrukcja uruchomienia, treningu i testów E2E](browser_demo/README.md).

## E3.1: symulacja H1 i odtwarzalność

h1_power.py: symulacja pełnych prób RT z heteroskedastycznością, zmiennymi kategorialnymi, błędami i QA oraz właściwym OLS HC3. Parametr beta_ms to nominalny efekt generatora przed selekcją, niekoniecznie prawdziwy estymand po QA. Przy nierzetelności GAD-7 pokrycie nominalnej wartości nie jest kalibracją CI obserwowanego efektu. Właściwa kampania i kalibracja pozostają bramką zamrożenia. Reproducibility: environment.py zapisuje SHA, wersje, zależności i hashe źródeł oraz opcjonalnego raportu. Uruchomienie lokalne, pliki wynikowe poza repozytorium:

```sh
.venv-anx/bin/python papers/cognition/MSC-ANX-P01/reference/h1_power.py --recruited 444 --repetitions 100 > /tmp/anx-h1.json
.venv-anx/bin/python papers/cognition/MSC-ANX-P01/reference/environment.py --report /tmp/anx-h1.json > /tmp/anx-h1-env.json
```
