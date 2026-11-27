# MSC-CR-P12 — Transfer odporności poznawczej między dziedzinami

**Właściciel naukowy i autor szkicu:** Mateusz Pomianek (`MatPomGit`). Współautorów należy wskazywać zgodnie z potwierdzonym wkładem; repozytorium kanoniczne jest odrębną informacją.

**Rodzaj pracy:** `IDEA`. **Etap badań:** `IDEA_REVIEW`.

[Manuskrypt LaTeX](main.tex) zawiera odrębny tytuł, pytanie badawcze i projekt analizy. Jest to szkic badawczy; brak w nim niezweryfikowanych wyników empirycznych.

Temat i status odpowiadają jednoznacznemu identyfikatorowi MSC w rejestrze portfolio. Materiały źródłowe i dowody eksperymentalne zachowują właściciela we właściwym projekcie badawczym.

## Strategia publikacyjna

[Szczegółowa strategia publikacyjna](journal-targets.md), opracowana 22.11.2026, wskazuje **Computers in Human Behavior** (140 pkt z wykazu 2024) jako cel główny, **British Journal of Educational Technology** (140 pkt) jako alternatywę edukacyjną oraz **Learning and Instruction** (200 pkt) jako ambitny cel warunkowy. Przed zgłoszeniem konieczne są: rygorystyczna ocena transferu między niećwiczonymi dziedzinami, odroczony pomiar, rozróżnienie selektywnej odporności od globalnej nieufności i ponowna kontrola punktacji.

## Pakiet prospektywny 1.0.0

[Protokół, słownik danych i plan OSF](protocol.md), [porównanie serii i literatury](novelty.md), [generator banku kandydackiego](materials.py), [lokalna demonstracja](demo.html) oraz [symulacja](simulation.py) z [wynikami syntetycznymi](power-synthetic.csv).

W katalogu manuskryptu uruchom `latexmk -norc -pdf main.tex`. Bank odtworzysz przez `python materials.py > items.json`. Zależności symulacji określa `requirements.txt`. Polecenia `python -B -m unittest discover` i `python -B simulation.py > power-synthetic.csv` odtwarzają testy oraz scenariusze planistyczne. Kontrola czułości i kryterium dotyczy reakcji na porady, a analiza mocy stosuje przybliżenie na poziomie osób.

[Model hierarchiczny](analysis_model.py) generuje ślad posterior z tabeli prób przygotowanej zgodnie z protokołem. Uruchomienie dopasowania wymaga dodatkowo PyMC 5 i środowiska rozwiązanego wspólnie z zależnościami PyMC. Test regresyjny obejmuje znaki i wagi kontrastu, a kalibracja całego dopasowania stanowi bramkę przed rekrutacją.

W 48 scenariuszach po 1200 replikacji (ziarno 27112026) dla latentnego efektu 0,20 i N=640 odsetek dodatnich rozstrzygnięć wyniósł 88,8% przy 15% MCAR i mniejszej zmienności pozycji oraz 76,2% przy 30% MCAR i większej zmienności. Przy efekcie 0,35 i N=480 odpowiadające wartości wyniosły 100,0% i 98,6%. Wyniki nie uzasadniają zamrożenia liczebności przed pilotażem i kalibracją modelu głównego.
