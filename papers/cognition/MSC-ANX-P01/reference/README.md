# Referencyjny model obliczeniowy MSC-ANX-P01

Właściciel naukowy: Mateusz Pomianek. Status: prospektywny model syntetyczny, nie aplikacja do zbierania danych. Kod jest publiczną ilustracją kontraktu i nie zastępuje przyszłego kanonicznego repozytorium badania.

- design.py: deterministyczny manifest 240 prób klasyfikacji (48 bazowych, 192 mieszane), 94 switch / 94 repeat, cztery nieokreślone pierwsze przejścia, 96 wyborów. Dokładnie 12 powtórzeń identycznego bodźca w każdym warunku. Marginesy są kontrolowane w całej sesji; generator przyjmuje wyłącznie sekwencje spełniające jawne tolerancje i przerywa po 128 nieudanych próbach. Wersja bodźców 0.4.1, wersja protokołu 0.4.0. Tolerancje są wstępnymi progami inżynieryjnymi, nie gwarantują pełnej ortogonalności ani rzetelności psychometrycznej. Ziarna 0–15 ilustrują 16 kombinacji przypisania odpowiedzi, kolejności bloków bazowych i kolejności zadań; w badaniu alokację trzeba równoważyć niezależnie od identyfikatora.
- audit_design.py: audyt 2048 kolejnych ziaren, zakresy marginesów i raport JSON; niezerowy kod wyjścia przy niepowodzeniu.
- synthetic.py: generowanie wyłącznie rekordów SYN, obliczanie median kosztu i bazowego RT, trafności i kwalifikacji. Minimum 24 poprawne bazowe próby jest dodatkowym proponowanym progiem. Timeout jest niepowodzeniem w analizie trafności, nigdy ważną poprawną reakcją. Nie przechowuje danych ani nie wysyła żądań sieciowych.
- power.py: analityczne przybliżenie Fishera i symulacja Monte Carlo zmiennej liczebności po niezależnej utracie; nie symuluje jeszcze rzetelności kosztu ani modeli H2/H3. Założenie r dotyczy korelacji częściowej obserwowanych zmiennych, nie efektu latentnego.

Uruchomienie z katalogu repozytorium:

```sh
python3 -B -m unittest discover -s tests -p test_anx_reference.py -v
python3 -B papers/cognition/MSC-ANX-P01/reference/audit_design.py --count 2048
python3 -B papers/cognition/MSC-ANX-P01/reference/power.py --recruited 444 --r .15 --repetitions 5000 --seed 42
```

Kolejne prace: niezależna weryfikacja generatora, symulacja niezależnych parametrów poziomu prób, pełne modele HC3 i GLMM oraz analiza rzetelności. Implementacja przeglądarkowa, zatwierdzone skale i akwizycja danych wymagają osobnego kanonicznego środowiska, testów timing i decyzji etycznej. Nie wdrażać na GitHub Pages.
