# Warunki rozpoczęcia zbierania danych

Aktualny status: **NIEGOTOWE DO STARTU**. Przygotowane dokumenty nie potwierdzają wykonania poniższych czynności. Lista dotyczy pracy badawczej, nie zatwierdzania zmian w GitHub.

| ID | Warunek | Dowód przed startem | Status |
|---|---|---|---|
| G01 | Osoba prowadząca, koderzy, opiekun danych i analityk przypisani | Prywatny rejestr ról i odpowiedzialności | otwarte |
| G02 | Procedura instytucjonalna/etyczna i zgoda uczestnika rozstrzygnięte | Właściwa decyzja lub udokumentowane ustalenie wymagań; finalna informacja dla uczestnika | otwarte |
| G03 | Plan przetwarzania i wtórnego użycia danych | Cele, dostęp, wycofanie, okres przechowywania, miejsce kopii, zakres udostępniania | otwarte |
| G04 | Rekrutacja, kwalifikacja i zakończenie naboru ustalone | Finalny tekst rekrutacji, formularz kwalifikacji, test rozdzielenia rund i osób | otwarte |
| G05 | Wersja planu zamrożona przed daną fazą | Commit, manifest SHA-256, datowana kopia/rejestracja i informacja o wcześniejszym dostępie do danych | otwarte |
| G06 | Koderzy przeszkoleni bez zmiany odpowiedzi uczestników | Niezależne kodowanie syntetycznego przykładu, uzgodnione rozbieżności w instrukcji | otwarte |
| G07 | Formularz i powiadomienia działają | Próbne przejście na docelowych telefonach, eksport według kontraktu, wycofanie i brak sieci | otwarte |
| G08 | Analiza działa na danych syntetycznych | Skrypt, wersje narzędzi i testy przypadków: 0 odpowiedzi, 100% sufitu, przerwanie, opóźnienie, duplikat, zero wariancji | **zamknięte technicznie** |
| G09 | Kopia i odtworzenie zbioru sprawdzone | Odtworzenie testowego eksportu i porównanie sum kontrolnych, bez danych ludzi w Git | otwarte |
| G10 | Bramka kognitywna dla ESM spełniona | Wyniki CA-Q1 na finalnej wersji, zgodnie z limitem rund | przed ESM |

Faza kognitywna wymaga G01–G06 i G09, a także sprawdzenia narzędzia zapisu kodowań. G07–G08 i G10 są wymagane przed ESM. W razie przerwania na wcześniejszej fazie zachować pełny raport z przyczynami; nie zastępować brakującej fazy symulowanymi „wynikami ludzi”.

G08 zamknięte technicznie dla kontraktu 0.1.0: walidacja czterech CSV, wybór prób, F1/F2/M1/M2, czasy pozycji, CA-D1 i bootstrap osobniczy są zaimplementowane i przeszły CI wraz z syntetycznym przebiegiem end-to-end. To nadal nie jest test działania formularza na telefonie. G07 pozostaje otwarte do czasu testów na docelowych telefonach, a G10 pozostaje otwarte do czasu CA-Q1 na finalnej wersji instrumentu.

## Próbny przebieg przed ESM

Na syntetycznych danych sprawdzić wszystkie dziesięć pozycji, pierwsze prompty dnia, zmianę dnia, niedostarczone powiadomienie, brak sieci, spóźnione wysłanie, pominięcie, dwukrotne wysłanie, przerwanie formularza i rezygnację przed końcem tygodnia. Wynik każdego przypadku musi odpowiadać `data_contract.md`; sama poprawność JSON nie testuje aplikacji.

## Zamrożenie

`freeze_ca_plan.py` tworzy i weryfikuje sumy plików planu. Manifest jest identyfikatorem pakietu, nie zgodą na badanie ani dowodem prerejestracji. Utrwalić go poza edytowalnym roboczym katalogiem z datą i commitem przed pierwszą osobą danej fazy. Nie nadpisywać manifestu po zmianie; stworzyć nową wersję i odnotować odstępstwo. Analizy po obejrzeniu danych zawsze wskazują używaną wersję i status eksploracyjny.

```bash
python software/tools/freeze_ca_plan.py --output /prywatna/sciezka/ca-plan-v1.json
python software/tools/freeze_ca_plan.py --verify /prywatna/sciezka/ca-plan-v1.json
```

Ścieżkę zastąpić własną. Wykonywać z głównego katalogu repozytorium, w jego `.venv`. Nie uruchamiano rekrutacji ani zewnętrznej prerejestracji w ramach przygotowania tych plików.
