# Materiały pilotażowe MSC-CR-P06

Wersja 0.1.0, 2026-11-24. Scientific owner: Mateusz Pomianek. Status: PROSPECTIVE / DRAFT_NOT_VALIDATED.

## Pliki

- [Bank pozycji](pilot-bank.json): trzy formy A, B i C, 24 pozycje każda, 8 kluczy U, 8 S i 8 N. Każda forma obejmuje po 8 pozycji z trzech domen i 6 pozycji z uzasadnieniem (po 2 dla każdego klucza).
- [Lekcje](lessons.json): dwie wersje interwencji, po 10 ekranów i 4 ćwiczenia z informacją zwrotną, planowany czas 15 minut.
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
