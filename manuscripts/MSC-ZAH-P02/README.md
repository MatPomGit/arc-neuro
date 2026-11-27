# MSC-ZAH-P02 — Dwuwymiarowa mapa doliny niesamowitości: realizm wyglądu i naturalność zachowania

**Właściciel naukowy i autor szkicu:** Mateusz Pomianek (`MatPomGit`). Współautorów należy wskazywać zgodnie z potwierdzonym wkładem; repozytorium kanoniczne jest odrębną informacją.

**Status:** `IDEA_HOLD`; prospektywna koncepcja. **Working title:** *The Two-Dimensional Social Uncanny Valley: Appearance Realism by Behavioral Naturalness*.

Czy realizm wyglądu postaci oraz naturalność jej ruchu niezależnie i interakcyjnie determinują oceny niesamowitości?

**H1:** Realizm wyglądu i naturalność ruchu oddziałują na subiektywną ocenę niesamowitości ponad ich niezależne efekty.

**H2:** Powierzchnia ocen może mieć lokalne maksima dyskomfortu, lecz istnienie takiej struktury nie jest przyjmowane z góry.

**Wynik główny:** Nieliniowy składnik interakcji A i B w ocenie niesamowitości; estymacja powierzchni z przedziałami niepewności.

**Odrębność:** Jest to mapa podstawowego efektu, nie test przyczynowego wpływu oczekiwań z P03 ani naturalnych profili komunikacji z P04.

[Manuskrypt LaTeX](main.tex), [plan badania](study.yaml), [bibliografia](references.bib). Wspólna platforma: [ST-08](https://github.com/MatPomGit/research-autopilot/blob/main/docs/portfolio/reorganizacja-systemu-badan/shared_research_platforms.md). Nie przedstawiono wyników ani zatwierdzonego protokołu.

## Symulacja wrażliwości

W systemie Windows uruchom `run_simulation.bat`. W pozostałych systemach wykonaj `python -m pip install -r requirements.txt`, a następnie `python simulate_power.py`. Tryb własny: `python simulation_menu.py`. Wyniki CSV i zbiorczy wykres PNG są zapisywane w `results/` i nadpisywane przy kolejnym uruchomieniu. Tryb pełny oznacza większą liczbę replikacji modelu wstępnego, a nie finalny model konfirmacyjny. Model zakłada ciągłe odpowiedzi, niezależne zestawy bodźców i sferyczność kontrastów. Nie zastępuje symulacji modelu porządkowego ze skrzyżowanymi efektami losowymi. Wyników nie zweryfikowano wykonawczo.
