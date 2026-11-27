# MSC-ZAH-P03 — Błędy predykcji społecznej i asymetria niedopasowania wyglądu i zachowania

**Właściciel naukowy i autor szkicu:** Mateusz Pomianek (`MatPomGit`). Współautorów należy wskazywać zgodnie z potwierdzonym wkładem; repozytorium kanoniczne jest odrębną informacją.

**Status:** `IDEA_HOLD`; prospektywna koncepcja. **Working title:** *Social Expectation Violations and Asymmetric Appearance-Behavior Mismatch*.

Czy ten sam klip docelowy wywołuje różne oceny po różnym kontekście oczekiwań i czy efekt zależy od kierunku niezgodności wyglądu z ruchem?

**H1:** Manipulacja oczekiwaniem społecznym zmieni ocenę niesamowitości dla identycznego docelowego zachowania.

**H2:** Niedopasowanie robotyczny wygląd z ludzkim ruchem nie będzie równoważne ludzkiemu wyglądowi z ruchem mechanicznym.

**Wynik główny:** Interakcja kontekstu oczekiwań oraz kierunku niedopasowania w ocenie niesamowitości klipu docelowego.

**Odrębność:** Praca testuje mechanizm predykcyjny, a nie tylko opisuje nieliniową powierzchnię ocen P02.

[Manuskrypt LaTeX](main.tex), [plan badania](study.yaml), [bibliografia](references.bib). Wspólna platforma: [ST-08](https://github.com/MatPomGit/research-autopilot/blob/main/docs/portfolio/reorganizacja-systemu-badan/shared_research_platforms.md). Nie przedstawiono wyników ani zatwierdzonego protokołu.

## Symulacja porządkowa w Pythonie

`python -m pip install -r requirements.txt`

`python simulate_power.py --n 80 --clips 24 --reps 100`

`python run_grid.py --reps 100`

Model PyMC wykorzystuje skrzyżowane efekty losowe i decyzję na podstawie przedziałów a posteriori. Nie jest to test ilorazu wiarygodności CLMM. Kalibracja częstości odrzuceń pod hipotezą zerową jest wymagana przed przyjęciem procedury konfirmacyjnej. Wyniki nie zostały jeszcze zweryfikowane wykonawczo.
