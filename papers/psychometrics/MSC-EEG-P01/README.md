# MSC-EEG-P01 — Kandydat: publikacja metod oprogramowania EEG Neurolyze

**Właściciel naukowy i autor szkicu:** Mateusz Pomianek (`MatPomGit`). Współautorów należy wskazywać zgodnie z potwierdzonym wkładem; repozytorium kanoniczne jest odrębną informacją.

**Rodzaj pracy:** `IDEA`. **Etap badań:** `PROPOSED`.

[Manuskrypt LaTeX](main.tex) zawiera odrębny tytuł, pytanie badawcze i projekt analizy. Jest to szkic badawczy; brak w nim niezweryfikowanych wyników empirycznych.

Temat i status odpowiadają jednoznacznemu identyfikatorowi MSC w rejestrze portfolio. Materiały źródłowe i dowody eksperymentalne zachowują właściciela we właściwym projekcie badawczym.

## Pakiet metod 1.0.0

[Manuskrypt](main.tex), [bibliografia](references.bib) i [wyniki benchmarku](spectral-benchmark.csv) opisują syntetyczną weryfikację implementacji Welcha w [źródle Neurolyze](https://github.com/MatPomGit/eeg-neurolyze/tree/fb9191f2710f642f91b2de60adfaba527a239496). Użyto Pythona 3.12, NumPy 2.3.5 i SciPy 1.17.0. Dane syntetyczne generuje [skrypt](spectral_benchmark.py) z ziarnem 27112026.

Z przypiętego checkoutu Neurolyze udostępnij katalog `src` przez `PYTHONPATH` i uruchom `python -B spectral_benchmark.py` w katalogu manuskryptu. W checkoutcie Neurolyze uruchom `PYTHONPATH=src python -B -m unittest discover -s tests -p 'test_spectral.py' -v` oraz analogiczny przebieg dla `test_eyes_open_closed.py`. Budowanie PDF uruchamia `latexmk -norc -pdf main.tex`. Wynik benchmarku dotyczy numerycznej zgodności na wejściach syntetycznych.
