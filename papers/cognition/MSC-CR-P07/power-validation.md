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
