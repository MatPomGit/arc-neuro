# Strategia publikacyjna: MSC-CR-P04

**Data weryfikacji:** 2026-11-22. **Wersja:** 1.0.0. **Status:** plan publikacyjny, bez zgłoszenia artykułu i bez danych empirycznych.

**Manuskrypt:** Ramowanie porad LLM i brakujący kontekst a rozpoznanie nieuprawnionych założeń.

## Ranking czasopism

| Priorytet | Czasopismo | ISSN | Punkty wykazu 2024 | Dopasowanie |
| --- | --- | --- | ---: | --- |
| 1, główny | Computers in Human Behavior | 0747-5632 | 140 | Psychologiczne mechanizmy oceny porad AI, poznawcza podatność na ramowanie i jakość osądu |
| 2, alternatywny | International Journal of Human-Computer Studies | 1071-5819 | 140 | Efekt prezentacji niepełnego kontekstu i informacji w interfejsie człowiek–AI; wymaga silnego wkładu HCI |
| 3, rezerwowy | Current Psychology | 1046-1310 | 70 | Eksperyment ogólnopsychologiczny z kontrolą treści i pomiarem rozumowania |

**Decyzja:** *Computers in Human Behavior* (140 pkt) jako pierwszy cel. *International Journal of Human-Computer Studies* (140 pkt) jako alternatywa przy silnym wyeksponowaniu problemu projektowania interfejsów i interakcji z LLM. *Current Psychology* (70 pkt) jako rezerwa.

## Główna propozycja metodologiczna

Plan eksperymentu **2 × 2**: kompletność informacji (kompletne versus brakujące przesłanki) × ramowanie porady LLM (neutralne versus perswazyjne). Wszystkie pozostałe właściwości zadania i odpowiedzi powinny być możliwie stałe. Stosować odmienne scenariusze problemowe oraz losowe zrównoważenie kolejności i warunków.

**Pierwszorzędowy estymand:** interakcja kompletności i ramowania na prawdopodobieństwo poprawnego wykrycia nieuprawnionego założenia. Konieczne jest ścisłe określenie, co oznacza „nieuprawnione założenie”, jak skonstruowano klucz odpowiedzi oraz co jest odpowiedzią poprawną w warunku pełnego kontekstu. Bez uwzględnienia poprawnych odrzuceń powstaje ryzyko mieszania czułości z tendencją do zgłaszania braków.

**Metryki drugorzędowe:** trafność decyzji, akceptacja porady mimo brakujących przesłanek, pewność osądu, czułość i specyficzność rozpoznawania luk, ewentualnie czas decyzji. Rozważyć teorię detekcji sygnałów, jeżeli liczba i struktura prób pozwalają na stabilną estymację.

**Analiza:** prerejestrowany mieszany model logistyczny z uczestnikiem i scenariuszem jako efektami losowymi, interakcją dwóch czynników i wcześniej określonymi kontrastami; ocena wielokrotności i wariantów analiz. Estymacja powinna mieć określony minimalny efekt istotny naukowo i uzasadnienie wielkości próby.

## Wymagania przed zgłoszeniem

1. Przygotować bank problemów z jednoznacznie zdefiniowaną prawdą zadania i kontrolą dziedziny, trudności, długości oraz tonu.
2. Oddzielić **perswazyjność wypowiedzi** od **jej faktograficznej poprawności**. Nie wolno zmieniać równocześnie argumentów, faktów i ramowania bez kontroli.
3. Zweryfikować manipulację ramowania w niezależnym pilotażu i ocenić rozumienie poleceń.
4. Zamrozić wersje modeli, teksty porad, prompty, bodźce i kod losowania; preferować stały zestaw odpowiedzi zamiast generacji na żywo.
5. Dodać próbę bez porady LLM albo kontrolę ludzkiej porady, jeżeli celem stanie się rozróżnienie efektu AI od ogólnego efektu perswazji.
6. Zapewnić zaślepioną ocenę odpowiedzi otwartych, zgodność między oceniającymi i oddzielenie ocen eksperckich od warunków.
7. Ustalić wymogi etyczne, ochronę danych, kryteria wykluczenia, plan mocy oraz prerejestrację.

## Ryzyka naukowe i redakcyjne

Eksperyment może sprowadzić się do ogólnego efektu perswazji, jeśli nie wykaże specyficznego wkładu HCI lub psychologii korzystania z LLM. Brak kontroli nieuprawnionych założeń może w rzeczywistości mierzyć wyłącznie nieufność uczestnika. Istnieje również możliwość efektów domeny, poziomu wiedzy i „pozytywnego” nastawienia do AI. Sama deklarowana pewność nie zastępuje behawioralnej trafności osądu. Wnioski przyczynowe mogą dotyczyć zrandomizowanych czynników, ale nie cech użytkownika ani długoterminowych skutków używania LLM.

## Koszty, punkty i status

Punktacja dotyczy wykazu ministerialnego z 5 stycznia 2024 r. i wymaga sprawdzenia przed publikacją w kolejnych latach. Preferowana jest tradycyjna ścieżka publikacji, jeżeli nie wymaga obowiązkowego APC; bieżące opłaty dodatkowe, wybór OA i umowy transformacyjne wymagają potwierdzenia w redakcji.

Manuskrypt ma status `PROSPECTIVE`. Nie ma zebranych danych, przeprowadzonego eksperymentu, decyzji redakcyjnej ani zatwierdzenia publikacji na GitHub Pages.

## Źródła

- [Computers in Human Behavior, strona wydawcy](https://shop.elsevier.com/journals/computers-in-human-behavior/0747-5632)
- [International Journal of Human-Computer Studies, strona wydawcy](https://shop.elsevier.com/journals/international-journal-of-human-computer-studies/1071-5819)
- [Current Psychology, strona wydawcy](https://link.springer.com/journal/12144)
- [Punktacja CHB, baza UJ](https://apacz.matinf.uj.edu.pl/czasopisma/227380-computers_in_human_behavior)
- [Punktacja IJHCS, baza UJ](https://virt3.matinf.uj.edu.pl/czasopisma/229628-international_journal_of_human_computer_studies)
- [Punktacja Current Psychology, baza APS](https://bw.aps.edu.pl/info/journalseries/WUT69407/)
