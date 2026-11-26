# Referencyjny model obliczeniowy MSC-ANX-P01

Właściciel naukowy: Mateusz Pomianek. Status: prospektywny model syntetyczny, nie aplikacja do zbierania danych. Kod jest publiczną ilustracją kontraktu i nie zastępuje przyszłego kanonicznego repozytorium badania.

- design.py: deterministyczny manifest 240 prób klasyfikacji (48 bazowych, 192 mieszane), 94 switch / 94 repeat, cztery nieokreślone pierwsze przejścia, 96 wyborów. Dokładnie 12 powtórzeń identycznego bodźca w każdym warunku. Marginesy są kontrolowane w całej sesji; generator przyjmuje wyłącznie sekwencje spełniające jawne tolerancje i przerywa po 128 nieudanych próbach. Wersja bodźców 0.4.1, wersja protokołu 0.4.0. Tolerancje są wstępnymi progami inżynieryjnymi, nie gwarantują pełnej ortogonalności ani rzetelności psychometrycznej. Ziarna 0–15 ilustrują 16 kombinacji przypisania odpowiedzi, kolejności bloków bazowych i kolejności zadań; w badaniu alokację trzeba równoważyć niezależnie od identyfikatora.
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
.venv-anx/bin/python -m pip install -r papers/cognition/MSC-ANX-P01/reference/requirements-analysis.txt
.venv-anx/bin/python -m unittest discover -s papers/cognition/MSC-ANX-P01/reference -p test_statistical.py -v
.venv-anx/bin/python papers/cognition/MSC-ANX-P01/reference/statistical.py --n 80 --seed 42
```

Bez utrwalania danych, tylko raport syntetyczny. Przypięto bezpośrednie zależności, nie pełne zależności przechodnie. Modele GLMM oraz analiza prób RT: mixed_models.py. Weryfikacja poprawności implementacji nie zastępuje walidacji modelu na zatwierdzonym protokole.

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

## Lokalny demonstrator przeglądarkowy (P3.6a)

Wygeneruj manifest w Pythonie, uruchom statyczny serwer wyłącznie na loopback i otwórz adres localhost. Wczytaj plik JSON ręcznie. Prototyp bez formularzy zdrowotnych, identyfikatorów uczestników, sieciowej akwizycji, pamięci trwałej, telemetrii i publikacji Pages. Eksport DEMO jest jawnie niezgodny z wejściem analiz syntetycznych. Nie udostępniać uczestnikom badania.

```sh
cd papers/cognition/MSC-ANX-P01/reference
python3 export_demo.py /tmp/anx-demo.json --seed 42
python3 -m http.server 8765 --bind 127.0.0.1 --directory browser_demo
# Otwórz http://127.0.0.1:8765/ w przeglądarce i wybierz /tmp/anx-demo.json.
# Testy kontraktu JS, Node >=20:
ANX_DEMO_MANIFEST=/tmp/anx-demo.json node --test browser_demo/core.test.mjs
```

Implementacja: 336 prób, mapowanie F/J, wskazówka 300 ms, deadline klasyfikacji 2000 ms, ITI 500 ms, przerwy między blokami, kontrola fokusu, odrzucanie powtórzonych zdarzeń klawiszy, rozróżnienie timeout i błędu technicznego. RT = timestamp zdarzenia klawiatury minus znacznik aktualizacji DOM w requestAnimationFrame; nie jest to potwierdzony fizyczny onset. Próg 150 ms nadmiarowego czasu wskazówki jest wstępny. Trening i sprawdzanie zrozumienia dodano w P3.6b; nadal brak końcowej walidacji timing na różnych przeglądarkach i gwarancji rzeczywistej ekspozycji. Przed pilotażem potrzebne: testy E2E w przeglądarce, kontrola urządzenia i opóźnień, zatwierdzone skale, instrukcje i zgoda etyczna. Nie zastępuje przyszłej aplikacji kanonicznej.

## Trening, kontrola rozumienia i E2E (P3.6b)

Manifest demonstratora v0.2.0: dwa osobne bloki treningu po 24 próby, z odrębnych ziaren zachowujących mapowanie klawiszy. Trening przed pierwszą próbą klasyfikacji (także gdy decyzje są pierwsze), wymagane 18 poprawnych odpowiedzi w przedziale 150–2000 ms; jedno powtórzenie. Błędy techniczne i timeout nie zaliczają próby treningowej. Brak zaliczenia drugiej próby kończy demonstrację. Przed pierwszym zadaniem decyzyjnym trzy pytania sprawdzające rozumienie prawdopodobieństw; po błędzie wyjaśnienie i ponowne podejście. Raport DEMO oddziela trening od 336 prób właściwych i zawiera diagnostykę czasu wskazówka–aktualizacja DOM, a nie fizyczny onset. Progi pozostają projektowe. Nie zbiera się danych uczestników.

Test E2E Chromium: `ANX_CHROME=/usr/bin/google-chrome python3 browser_demo/e2e.py` (w izolowanym venv z playwright==1.56.0). CI używa przeglądarki Chrome z obrazu publicznego runnera, bez publikacji. Kontrolowane zdarzenie blur testuje reakcję kodu, nie rzeczywiste opóźnienie przełączenia okna. Przed badaniem pozostaje walidacja wieloprzeglądarkowa i sprzętowa, audyt dostępności, instrukcje, zgoda etyczna i kanoniczne środowisko. 
