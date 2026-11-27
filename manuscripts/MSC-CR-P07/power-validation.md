# Walidacja analizy mocy MSC-CR-P07

Data: 2026-11-26. Właściciel naukowy: Mateusz Pomianek.

## Środowisko i identyfikacja

Kod po poprawce API: commit defbb84422010580d037f7f356f1f2fbd116801a.
Git blob skryptu: 2b2a37e26708d703a43715a14ad434a59bea7ac5.
Git blob testów: eb9573bd38772992f3bab43b86af876b908cb184.
Oba lokalne pliki zweryfikowano przez git hash-object.
NumPy 2.3.5, pandas 2.2.3, SciPy 1.17.0, statsmodels 0.14.6.
OPENBLAS_NUM_THREADS=1, OMP_NUM_THREADS=1.

## Testy

Przed poprawką: 6/6 PASS, lecz rzeczywiste dopasowanie zgłaszało TypeError:
fit_vb nie obsługuje argumentu method. Zmieniono go na fit_method.
Po poprawce i dodaniu rzeczywistego dopasowania: 7/7 PASS (0,237 s).

## Diagnostyka symulacyjna

Dwa scenariusze, po 20 replikacji, seed 20261126, n=80, 24 zadania,
alpha=logit(0.2), SD osoby=0.5, SD zadania=0.3,
początkowa trafność=0.75, brak danych=0.

| OR | Odrzucenia | Nieudane | Bias beta | RMSE | Pokrycie | 95% CI odrzuceń |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| 1.0 | 2/20 | 0/20 | -0.089824 | 0.196543 | 0.90 | 0.01235–0.31698 |
| 1.6 | 19/20 | 0/20 | -0.053735 | 0.168817 | 0.85 | 0.75127–0.99873 |

Odtworzenie w katalogu manuskryptu:

    python -m unittest -v
    python -c "import power_simulation as p; import numpy as np; print(p.scenario(80,24,0,.5,.3,.75,0,20,20261126)); print(p.scenario(80,24,np.log(1.6),.5,.3,.75,0,20,20261126))"

## Interpretacja

Wstępna diagnostyka wskazuje na konieczność dalszej kalibracji.
Normalne przybliżenie posterioru VB nie jest skalibrowanym testem częstotliwościowym.
Przed ustaleniem liczebności należy porównać kalibrację na większej liczbie
replikacji oraz uwzględnić marginalny estymand różnicy ryzyka.
Nie zatwierdzono liczebności rekrutacyjnej. Status PROSPECTIVE pozostaje bez zmian.

## E3.1: zmiana procedury pierwszorzędowej

Wersja 0.2.2: estymator Hájeka, klastrowanie uczestników, ustalony bank zadań.
Wcześniejszy plik power_grid.json (blob 22edec8) obejmuje 25 scenariuszy po 200 replikacji, seed 20261126, 24 zadania, SD osoby 0.5, SD zadania 0.3, trafność 0.75, brak danych 0. Odpowiada historycznej wersji randomization_power.py (blob 75323857c9391773c04ec92f1336e6ea54ab5dd7), dostępnej w HEAD 60bee60acaaaa012d4edc4788450c74a1ce9ce07. Odtworzenie z tej rewizji:

    python randomization_power.py --grid --replicates 200 --seed 20261126 --output power_grid.json

Nie potwierdzono niezależnie środowiska tej historycznej siatki ani identyczności wyników. Nie używać jej do wyboru liczebności w zmienionym schemacie Bernoulliego.

Aktualny kod: marginal_rd.py (blob c217cd2a08c9f83d3676a1e6d16014b69d1d2c84), rd_power.py (blob bbca1e9b5ee4d684cca0457124ddd4d7bf785dd2).
Odtworzenie z aktualnego katalogu (w izolowanym środowisku):

    python -m unittest -v test_marginal_rd test_rd_power test_randomization_power
    python rd_power.py --smoke --replicates 1000 --seed 20261126 > rd-smoke.json
    python rd_power.py --replicates 1000 --seed 20261126 > rd-grid.json

Siatka 192 scenariuszy: N 80/160/240, RD 0/.03/.05/.08, SD osoby .5/1, SD zadania .3/.7, trafność .55/.75, MCAR 0/.1. Każdy scenariusz warunkowy względem wygenerowanego banku; niepewność Monte Carlo: dokładne przedziały dwumianowe. Nieudane dopasowania liczone jako brak odrzucenia; pokrycie warunkowe względem udanych estymacji, z osobną częstością niepowodzeń. Moc H1 oznacza dolną granicę CI > 0. Dopuszczalny kierunkowy błąd I rodzaju wynika z dwustronnego CI 95% (0.025). Próg minimalnego RD i liczebność pozostają decyzjami przed prerejestracją.

Bibliografia: DOI 10.1016/j.chb.2024.108352, 10.1145/3581641.3584066, 10.1145/3449287, 10.1145/3630106.3658941 zweryfikowane w metadanych wydawców 2026-11-26. Zakres: koszty nadmiernego polegania, adekwatne poleganie, interwencje cognitive forcing, językowa niepewność w zadaniach medycznych. Nie jest to systematyczny przegląd literatury.

Status: PROSPECTIVE. Nowa pełna siatka i CI wymagają wykonania; nie deklaruje się wyników, których nie uzyskano.
