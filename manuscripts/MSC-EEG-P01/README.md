# MSC-EEG-P01 — Kandydat: publikacja metod oprogramowania EEG Neurolyze

**Właściciel naukowy i autor szkicu:** Mateusz Pomianek (`MatPomGit`). Współautorów należy wskazywać zgodnie z potwierdzonym wkładem; repozytorium kanoniczne jest odrębną informacją.

**Rodzaj pracy:** `IDEA`. **Etap badań:** `PROPOSED`.

[Manuskrypt LaTeX](main.tex) zawiera odrębny tytuł, pytanie badawcze i projekt analizy. Jest to szkic badawczy; brak w nim niezweryfikowanych wyników empirycznych.

Temat i status odpowiadają jednoznacznemu identyfikatorowi MSC w rejestrze portfolio. Materiały źródłowe i dowody eksperymentalne zachowują właściciela we właściwym projekcie badawczym.

## Pakiet metod 1.0.0

[Manuskrypt](main.tex), [bibliografia](references.bib) i [wyniki benchmarku](spectral-benchmark.csv) opisują syntetyczną weryfikację implementacji Welcha w [źródle Neurolyze](https://github.com/MatPomGit/eeg-neurolyze/tree/fb9191f2710f642f91b2de60adfaba527a239496). Użyto Pythona 3.12, NumPy 2.3.5 i SciPy 1.17.0. Dane syntetyczne generuje [skrypt](spectral_benchmark.py) z ziarnem 27112026.

Z przypiętego checkoutu Neurolyze udostępnij katalog `src` przez `PYTHONPATH` i uruchom `python -B spectral_benchmark.py` w katalogu manuskryptu. W checkoutcie Neurolyze uruchom `PYTHONPATH=src python -B -m unittest discover -s tests -p 'test_spectral.py' -v` oraz analogiczny przebieg dla `test_eyes_open_closed.py`. Budowanie PDF uruchamia `latexmk -norc -pdf main.tex`. Wynik benchmarku dotyczy numerycznej zgodności na wejściach syntetycznych.

## Odtwarzanie benchmarku i testy brzegowe

W powłoce Bash, z katalogu manuskryptu, przy dostępie do repozytorium Neurolyze:

```bash
python3.12 -m venv .venv
. .venv/bin/activate
python -m pip install numpy==2.3.5 scipy==1.17.0
python -m pip check
git clone https://github.com/MatPomGit/eeg-neurolyze.git /tmp/neurolyze-eeg-p01
git -C /tmp/neurolyze-eeg-p01 checkout --detach fb9191f2710f642f91b2de60adfaba527a239496
test "$(git -C /tmp/neurolyze-eeg-p01 rev-parse HEAD)" = fb9191f2710f642f91b2de60adfaba527a239496
export PYTHONPATH=/tmp/neurolyze-eeg-p01/src
python -B spectral_benchmark.py > /tmp/eeg-p01-replay.csv
cmp spectral-benchmark.csv /tmp/eeg-p01-replay.csv
python -B -m unittest discover -s . -p 'test_spectral_edges.py' -v
````

Porównanie bajtowe dotyczy przypiętego środowiska; różnice między platformami należy oceniać również względem tolerancji numerycznej. Testy brzegowe nie stanowią walidacji klinicznej ani walidacji EEG-BIDS.
