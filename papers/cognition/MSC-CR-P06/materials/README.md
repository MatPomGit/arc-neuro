# Materiały pilotażowe MSC-CR-P06

Wersja 0.3.0, 2026-11-24. Scientific owner: Mateusz Pomianek. Status: PROSPECTIVE / DRAFT_NOT_VALIDATED.

## Pliki

- [Bank pozycji](pilot-bank.json): trzy formy A, B i C, 24 pozycje każda, 8 kluczy U, 8 S i 8 N. Każda forma obejmuje po 8 pozycji z trzech domen i 6 pozycji z uzasadnieniem (po 2 dla każdego klucza).
- [Lekcje](lessons.json): dwie wersje interwencji, po 10 ekranów i 4 ćwiczenia z informacją zwrotną, planowany czas 15 minut.
- [Moduł punktowania](scoring.py): referencyjne obliczenia w Pythonie, bez zależności zewnętrznych.
- [Formularz ekspercki](expert-review.csv): 72 pozycje bez klucza autorskiego, puste pola oceny.
- [Psychometria i planowanie](psychometrics.py): klasyczna teoria testów, porównanie form i scenariusze liczebności.
- [Manuskrypt](../main.tex): kanoniczny opis hipotez, miar i analizy w obrębie obecnego szkicu.

Bank jest jawny i zawiera klucz. Nie wolno użyć go bez zmian jako zamrożonego testu głównego. Wszystkie scenariusze są fikcyjne. Przed badaniem głównym należy stworzyć odrębne formy z ograniczonym dostępem, udokumentować ich wersję, przeprowadzić niezależną ocenę i pilotaż. Nie publikować kluczy zamrożonego testu przed zamknięciem akwizycji. Jawny bank pozwala sprawdzić procedurę i strukturę danych, ale nie potwierdza trafności psychometrycznej.

## Instrukcja testu dla uczestnika

Przeczytaj opis sytuacji oraz oceniane twierdzenie. Przyjmij podane informacje jako prawdziwe. Oceniaj wyłącznie to, czy twierdzenie wynika z opisu; nie uzupełniaj go wiedzą zewnętrzną.

- U: twierdzenie musi być prawdziwe przy podanych przesłankach.
- S: twierdzenie musi być fałszywe przy podanych przesłankach.
- N: dostępne przesłanki nie rozstrzygają, czy twierdzenie jest prawdziwe, czy fałszywe.

Następnie wskaż prawdopodobieństwo, że wybrana odpowiedź jest poprawna (0–100%). W niektórych zadaniach uzasadnij wybór w jednym lub dwóch zdaniach. Możesz pominąć pozycję. Nie korzystaj z AI, wyszukiwarki ani pomocy innych osób. W czasie testu nie otrzymasz informacji o poprawności. Przed właściwym testem pokaż trzy przykłady instruktażowe z odrębnej puli, identyczne dla obu grup.

## Procedura

Losować przydział interwencji w obrębie warstw doświadczenia z AI. Niezależnie równoważyć kolejność form ABC, ACB, BAC, BCA, CAB, CBA w obu ramionach. Przydział po preteście ma być ukryty do zakończenia tego pomiaru; formę pretestu przydzielać przed jego rozpoczęciem. Losować kolejność pozycji i odpowiedzi, przechowując stabilne identyfikatory i kody, a nie numery ekranów.

Lekcje mają ten sam układ, liczbę pytań, pojedynczą próbę odpowiedzi i moment informacji zwrotnej. W pilotażu mierzyć rzeczywisty czas, wysiłek, zainteresowanie i oczekiwania uczestników. Pytania kontrolne są prostsze od części ćwiczeń interwencyjnych; równoważność obciążenia nie jest wykazana. W razie rozbieżności zmodyfikować materiał i powtórzyć pilotaż. Zadania testowe mają inną treść niż lekcje, ale częściowo wspólną strukturę rozumowania; nie stanowią dowodu dalekiego transferu.

## Punktowanie i dane

Jedna obserwacja pozycji: pseudonim, punkt T0/T1/T2, identyfikator formy i pozycji, kod odpowiedzi U/S/N lub brak, pewność 0–100 lub brak, czas odpowiedzi, uzasadnienie tylko dla oznaczonych pozycji. Oddzielnie: losowy przydział, warstwa i kolejność form. Nie zapisywać kontaktu z uczestnikiem w zbiorze odpowiedzi. Klucz i grupa nie są prezentowane osobom oceniającym w sposób ujawniający przydział; oceniający potrzebuje przesłanek, twierdzenia i klucza treściowego.

Trafność = liczba poprawnych / liczba udzielonych odpowiedzi, minimum 20 z 24. Brier = średnia (pewność/100 − poprawność)^2, minimum 20 kompletnych par. Nadmierna pewność = średnia (pewność/100 − poprawność) dla tych samych par. Macierz pomyłek: wiersz rzeczywisty klucz, kolumna wybrana kategoria; raportować braki osobno. U→N i U→S opisują odrzucanie uzasadnionych twierdzeń; nie utożsamiać ich z samą nieufnością wobec AI.

Rubryka uzasadnień: 0 = odpowiedź niezwiązana z przesłanką lub błędne rozumowanie bez istotnej przesłanki; 1 = wskazanie istotnej przesłanki albo brakującej informacji bez poprawnego połączenia z decyzją; 2 = poprawne wyjaśnienie związku między przesłanką a wnioskiem, zgodne z kluczem. Nie wymagać dosłownego brzmienia klucza. Pusty tekst = brak, nie 0. Średnia z co najmniej 5 z 6 ocen. Dwóch oceniających koduje niezależnie; raportować ważoną kappę z wagami kwadratowymi i przedziałem ufności przed uzgodnieniem rozbieżności.

## Bramki pilotażu

Przynajmniej dwóch ekspertów ocenia klucz i jednoznaczność bez podpowiedzi; rozbieżne pozycje poprawić, nie rozstrzygać głosowaniem bez uzasadnienia. Pilotaż poznawczy 8–12 osób, ilościowy około 60 osób. Sprawdzić trudność (roboczo 0,25–0,90), skorygowaną korelację pozycja–wynik, rozkład kategorii, efekty sufitu i podłogi, czas, rzetelność i porównywalność form. Proste zadania mogą wykazywać sufit; dopiero pilotaż określi konieczny poziom trudności. Przy N≈60 nie traktować parametrów pozycji jako precyzyjnych. Wersja końcowa, liczebność, plan analizy i procedura etyczna wymagają zatwierdzenia przed rekrutacją główną. Nie przeprowadzono pilotażu ani badania głównego.

## Ocena ekspercka

Każdy ekspert otrzymuje osobną kopię formularza CSV, bez dostępu do banku z kluczem ani ocen drugiej osoby. Wypełnia samodzielnie kategorię U/S/N, uzasadnienie i ocenę jasności (1: niejednoznaczna, 4: całkowicie jednoznaczna), trafności treściowej (1: nieadekwatna, 4: bardzo adekwatna) i przewidywanej trudności (1: bardzo łatwa, 4: bardzo trudna). Przy ocenach 1–2 jasności lub trafności podaje propozycję zmiany. Koordynator porównuje klucze i uzasadnienia dopiero po zamknięciu ocen. Zgodność kategorii raportować jako procent i nieważoną kappę Cohena; dla trafności opisać odsetek ocen 3–4 dla każdej pozycji, bez traktowania dwóch ekspertów jako wystarczającego dowodu walidacji. Rozbieżności rozstrzygać merytorycznie, a poprawione pozycje ocenić ponownie. Nie gromadzić w publicznym repozytorium wypełnionych formularzy ani danych ekspertów.

## Referencyjne obliczenia

Uruchom z katalogu głównego repozytorium: `python -B -m unittest discover -s tests -p test_p06_scoring.py -v`. Moduł `scoring.py` udostępnia `load_bank()`, `score_form(items, rows)` i `quadratic_kappa(pairs)`. Funkcja punktowania przyjmuje dane pojedynczej osoby, formy i pomiaru; agregacja i kontrola przydziału są odrębnym etapem. Dane wejściowe nie mogą mieszać uczestników ani pomiarów. Brak odpowiedzi jest reprezentowany przez None albo brak wiersza. Niepoprawne kody, powtórzone identyfikatory, pewność poza zakresem oraz oceny uzasadnień dla nieoznaczonych pozycji są odrzucane. Oceny uzasadnień muszą pochodzić od ludzi; moduł nie ocenia tekstu automatycznie. Kappa bez zmienności oczekiwanej jest niezdefiniowana (None). Testy syntetyczne sprawdzają implementację, nie trafność psychometryczną.

## Psychometria i liczebność

Dla każdej formy raportować trudność jako odsetek poprawnych odpowiedzi wśród dostępnych odpowiedzi, z przedziałem Wilsona, skorygowaną korelację pozycji z sumą pozostałych pozycji i KR-20 na kompletnych formularzach. Podawać liczebności osobno, brakujące wyniki, odsetki pełnych wyników minimalnych i maksymalnych oraz bootstrapowy przedział KR-20 (1000 resampli uczestników; niezdefiniowane repliki raportowane, przedział pomijany przy mniej niż 90% poprawnych replik). Ujemna rzetelność lub dyskryminacja nie są obcinane do zera. Progi trudności i dyskryminacji są flagami do przeglądu, nie automatycznym kryterium usuwania pozycji.

W pilotażu porównać A/B/C u tych samych osób w sześciu zrównoważonych kolejnościach; rejestrować przerwy i obciążenie, nie stosować lekcji między formami. Raportować sparowane różnice, SD różnic, korelacje i wyniki według kolejności. Porównanie opisowe nie potwierdza równoważności; formalne kryterium równoważności wymaga uprzednio uzasadnionego marginesu i odpowiedniej mocy. Przy małej próbie szerokie przedziały są spodziewane.

Plan liczebności: normalne przybliżenie ANCOVA dla dwóch równych grup, d na skali marginalnego SD posttestu, korelacja pre/post rho, wariancja reszt 1-rho², alfa 0,05 i moc 0,80. Przy d=0,35 i 15% utracie: rho=0 / 0,3 / 0,5 / 0,7 daje odpowiednio 304 / 276 / 230 / 156 rekrutowanych. To analiza wrażliwości, nie wyniki pilotażu. Symulacja Monte Carlo generuje gaussowskie pre/post i estymuje ANCOVA z normalnym progiem krytycznym; nie modeluje ograniczonej skali trafności ani informacyjnych braków. Ostateczne N wymaga uzasadnienia efektu minimalnego i symulacji adekwatnej do rozkładu oraz mechanizmu braków.

Testy: `python -B -m unittest discover -s tests -p test_p06_psychometrics.py -v`. Dane syntetyczne nie są dowodem trafności narzędzia.
