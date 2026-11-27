# CA: walidacja eksportu i pierwsze analizy opisowe

Działający pakiet oparty na bibliotece standardowej Pythona. Nie wymaga stosu GEE H1 i nie uruchamia Monte Carlo. Dane wejściowe i raporty są **prywatne**. Kod, testy i generator są publiczne; generator tworzy wyłącznie oznaczone dane syntetyczne.

## Zakres wykonany

- Ścisła kontrola czterech CSV, kluczy, kompletności 42 zaplanowanych promptów na rozpoczętą osobę, wersji instrumentu, chronologii, zakresów i braków strukturalnych.
- Pierwsze terminowe wysłanie wyznaczane po czasie wysłania, niezależnie od kolejności w CSV. Remis czasów wymaga wyjaśnienia w źródle. Formularze późne, przerwane, po rezygnacji i duplikaty nie zwiększają realizacji.
- CA-F1: dokładne liczniki i mianowniki na osobę, również przy zerze odpowiedzi; osobno pełny plan, okres do rezygnacji i potwierdzone dostarczenia.
- CA-F2: surowe czasy formularzy oraz czasy pojedynczych pozycji od wyświetlenia do odpowiedzi, osobno dla wszystkich/wybranych prób i typów zakończenia; liczba nieobserwowanych czasów jest zachowana.
- CA-M1/M2: braki wśród wyświetlonych pozycji, rozkłady wartości, sufit/podłoga, udział wartości brzegowych oraz SD na osobę przy wymaganym minimum ocen.
- CA-D1: trzy zaplanowane korelacje opisowe (`C_state–A_state`, `A_state–W_solitude`, `A_state–X_distance`), osobno między średnimi osobniczymi i po centrowaniu wewnątrzosobniczym, z jawnymi liczebnościami osób i par.
- Niepewność: deterministyczny bootstrap całych osób dla median zaplanowanych wskaźników wykonalności, zgodnie z `design_config.json`; przy zbyt małej liczbie osób przedział pozostaje `null`.
- Prywatny rejestr kwalifikacji każdej próby oraz SHA-256 wejściowych plików, konfiguracji i kodu analizy. Brak imputacji i automatycznej naprawy błędnych danych.

W źródłowym repozytorium techniczna bramka G08 była zamknięta dla tego kontraktu eksportu; po migracji wymaga ponownego potwierdzenia. Testy CI obejmują walidację, syntetyczny przebieg end-to-end, czasy pozycji, bootstrap i CA-D1. CA-Q1 pozostaje odrębną bramką G10 opartą na rzeczywistych wywiadach kognitywnych i nie może zostać zastąpiona danymi syntetycznymi. Raport nie wylicza jednego automatycznego werdyktu „badanie gotowe”, ponieważ domeny wykonalności muszą być interpretowane oddzielnie wraz z governance i CA-Q1. Walidator nie sprawdza prawdziwości zdarzeń raportowanych przez telefon, zgód ani prywatności każdej dowolnej wartości identyfikatora. Nie jest systemem do zbierania danych.

## Próbny przebieg od głównego katalogu repozytorium

Użyć `.venv` repozytorium. Poniższe katalogi muszą jeszcze nie istnieć; zmień nazwy przy kolejnym przebiegu.

```bash
python manuscripts/MSC-ATTACH-P06/analysis/synthetic.py --output build/ca_synthetic/export
python manuscripts/MSC-ATTACH-P06/analysis/analysis.py --input build/ca_synthetic/export --output build/ca_synthetic/report
python -m unittest discover -s manuscripts/MSC-ATTACH-P06/analysis -p "test_analysis.py" -v
```

Oczekiwany wynik przykładu: jedna syntetyczna osoba, 42 prompty, 2 wybrane wysłania, 1 duplikat, 1 spóźnione wysłanie i 1 przerwana próba. Brak potwierdzonych dostarczeń daje `null` dla realizacji wśród potwierdzonych dostarczeń, nie 100%. Żadna liczba nie jest wynikiem badania ludzi.

Eksport rzeczywisty wymaga tych samych kolumn i warunków [kontraktu](../protocol/data_contract.md). Program czyta cztery tabele; `changes.csv` jest odrębnym dziennikiem pochodzenia, nie źródłem automatycznej korekty surowych wartości. Wszystkie cztery tabele muszą istnieć także przy braku odpowiedzi. Dokładne nagłówki tworzy generator; nie korzystać z plików syntetycznych jako szablonu do ręcznego dopisywania ludzi.

Analiza kończy się kodem 2 przy błędzie, zanim utworzy raport analityczny. Istniejący katalog wynikowy nie jest nadpisywany. Identyfikatory pseudonimowe pozostają w wynikach do kontroli wyboru prób: nie publikować `report.json` bez osobnej kontroli agregacji i prywatności.


Proweniencja: Mateusz Pomianek, ARC Attachment Dynamics, rewizja `9ddb0708dfcd380bcdc5a33f3a52d3b3c8df4b62`. Kod Apache-2.0 ([licencja](LICENSE)); opis CC-BY-4.0 ([licencja](../LICENSE-CC-BY-4.0.txt)). Zmieniono ścieżki konfiguracji i polecenia. Nie przeniesiono danych uczestników ani wyników jednostkowych.
