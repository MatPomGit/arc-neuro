# Analiza statystyczna MSC-CR-P06

Wersja 0.1.0, 2026-11-24. Właściciel naukowy: Mateusz Pomianek. Status: PROSPECTIVE / REFERENCE_IMPLEMENTATION. Brak wyników empirycznych i zatwierdzonego protokołu.

## Kontrakt danych

Jeden wiersz na losowo przydzieloną osobę. Pola: participant_id (pseudonim), arm (0 kontrola, 1 interwencja), stratum (0/1 według zamrożonej reguły doświadczenia), sequence (ABC/ACB/BAC/BCA/CAB/CBA), accuracy_T0/T1/T2, brier_T0/T1, justification_T0/T1. Trafność i Brier w [0,1], uzasadnienie w [0,2]. None oznacza brak. Brak danych kontaktowych. Wiersz zachować także po rezygnacji z posttestu, o ile uczestnik zezwolił na zachowanie danych. Wycofanie zgody obsłużyć zgodnie z zatwierdzoną procedurą, nie przez automatyczną imputację niedostępnych danych.

## Estymacja

analysis.py: ANCOVA z wyrazem wolnym, przydziałem, wycentrowanym odpowiednim pretestem, warstwą i pięcioma wskaźnikami kolejności (ABC jako referencja). HC3 z asymptotycznym rozkładem normalnym. Efekty H1/H2 w punktach procentowych; H3/H4 w jednostkach miary. H1 dwustronne alfa 0,05; trzy testy drugorzędowe z korektą Holma. Brak automatycznego usuwania zmiennych w razie osobliwości macierzy: przerwać i udokumentować problem przed dostępem do wyników. Przedziały 95% są marginalne, nie jednoczesne.

analyze_complete_cases jest analizą wrażliwości, a nie ITT przy brakach. analyze_imputations przyjmuje 50 zewnętrznie wygenerowanych kompletnych zbiorów i sprawdza identyczność uczestników, przydziału, warstwy, kolejności oraz zachowanie wszystkich obserwowanych wartości. Reguły Rubina: średnia estymat, średnia wariancja wewnątrz imputacji i (1+1/m) razy wariancja między imputacjami. Obecnie przedziały asymptotyczne, bez korekty małopróbkowej Barnarda–Rubina. Nie generuje imputacji; nie traktować powielonych zbiorów jako 50 prawidłowych imputacji.

Analiza MNAR: przesunąć tylko imputowane wyniki accuracy_T1 w jednym ramieniu o -0,05 lub -0,10, ograniczając do [0,1], osobno dla interwencji i kontroli. Te wartości są propozycją do zamrożenia. Zachować wyniki pozostałych hipotez. Raportować odsetek braków i wpływ założenia, a nie wnioskować o faktycznym mechanizmie MNAR.

## Raport

reporting.py zapisuje effects.csv i effects.svg; trzy odrębne skale, efekt interwencja minus kontrola, przedziały 95%, jawne oznaczenie źródła SYNTHETIC/PILOT/MAIN. Nie umieszczać danych uczestników ani wypełnionych formularzy w publicznym repozytorium. Wykres publikacyjny wymaga jeszcze recenzji po uzyskaniu rzeczywistych wyników.

## Bramki przed analizą empiryczną

- Zweryfikować skoring, eksport i kompletną ścieżkę danych; zachować manifest wersji i nasiona generatorów.
- Wdrożyć i zwalidować właściwe generowanie 50 imputacji PMM z odpowiednimi predyktorami, diagnostyką zbieżności i analizą stabilności; nie zastępować go średnią ani pojedynczą imputacją.
- Wdrożyć model logistyczny na poziomie pozycji oraz standaryzację predykcji. Ustalić procedurę przy problemach zbieżności.
- Zweryfikować właściwości HC3, Rubin pooling i procedurę przy małym N w symulacji ograniczonych wyników. Porównać implementację z niezależnym pakietem statystycznym.
- Zamrozić plan, przejść ocenę etyczną i pilotaż, dopiero wtedy analizować dane główne.

Testy: `python -B -m unittest discover -s tests -p 'test_p06*.py' -v`. Testy syntetyczne nie stanowią walidacji empirycznej.
