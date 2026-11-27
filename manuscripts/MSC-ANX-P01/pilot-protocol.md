# MSC-ANX-P01: protokół pilotażu v0.1.0

Scientific owner: Mateusz Pomianek. PROSPECTIVE, 2026-11-26. Pilotażu nie rozpoczęto.

## Cel
Ocena wykonalności, zrozumienia, jakości danych i rzetelności. Bez testowania H1–H3 i wyboru efektu na podstawie obserwowanej korelacji GAD-7 z zachowaniem. Proponowana liczebność 40 osób; ostatecznie zatwierdzić przed rekrutacją. Próba odrębna od konfirmacyjnej. Opcjonalna druga sesja w odstępie 7–14 dni u podgrupy, z odrębną zgodą i bez danych kontaktowych w repozytorium.

## Procedura
Po zatwierdzeniu etyki, administratora i aplikacji: informacja, zgoda, kontrola pełnoletności, polskiego i fizycznej klawiatury, test fokusu oraz urządzenia. Zatwierdzone wersje GAD-7 i skali depresyjności, wiek i sen. Alokacja blokowa do kombinacji mapowań i kolejności, oddzielona od pseudonimu. Właściwy manifest z przypiętego generatora. Trening z feedbackiem, jedna powtórka; bez feedbacku w próbach właściwych. Kontrola rozumienia decyzji przed ich rozpoczęciem, najwyżej dwa podejścia; niezaliczenie treningu lub quizu pomija odpowiednią grupę zadań, nie kończy automatycznie sesji. Równoważyć kolejność obu domen decyzji. Przerwy między blokami, możliwość przerwania. Zadania zgodnie z prospektem, debriefing. Nie używać obecnego demonstratora do akwizycji badawczej; brak zatwierdzonych formularzy i produkcyjnego zapisu.

## Proponowane kryteria przejścia
| Miernik | Próg do zatwierdzenia przed pilotażem | Działanie przy niespełnieniu |
|---|---|---|
| Ukończenie obu zadań | >=80% rozpoczynających | diagnoza czasu i obciążenia |
| Zaliczenie treningu do drugiej próby | >=90% | poprawić instrukcję i trening |
| Zrozumienie loterii do drugiego podejścia | >=90% | uprościć prezentację, ograniczyć próby quizu |
| Kwalifikacja H1 | >=80% rozpoczynających klasyfikację | przeanalizować błędy i timing |
| Kwalifikacja H2 i H3 | >=80% rozpoczynających daną domenę | poprawić instrukcję/QA |
| Próby technicznie nieważne | mediana odsetka <=5% w zadaniu | audyt aplikacji i urządzeń |
| Rzetelność SC | SB >=0,70 i dolne CI >=0,50 (orientacyjne) | więcej prób, poprawa paradygmatu, nowy pilotaż |
| Zróżnicowanie wyborów | ocena rozkładu 12 komórek, brak skrajnej dominacji wszystkich komórek | zmienić poziomy wypłat, ponownie sprawdzić identyfikowalność |

Progi nie są zwalidowanymi normami. Dla małego pilotażu podać przedziały niepewności i liczebności mianowników. Nie stosować ich mechanicznie bez oceny źródła problemu. Planowany czas 30–40 min zweryfikować na danych; preferować skrócenie obciążenia bez utraty jakości. Nie używać kosztu przełączania względem GAD-7 do decyzji o przejściu.

## Techniczna walidacja przed udziałem ludzi
- E2E w izolowanej przeglądarce: trening, niezaliczenie, quiz, przerwy, deadline, błędy, utrata fokusu, podwójne klawisze, przerwanie, eksport i brak transmisji nieautoryzowanej.
- Matryca Chrome/Firefox/Edge, co najmniej dwa typy komputerów i częstotliwości odświeżania; wersje udokumentowane. Fizyczny timing: pomiar onset ekranu i odpowiedzi referencyjnej urządzeniem lub metodą o udokumentowanej rozdzielczości; oddzielić opóźnienie stałe, jitter i różnice warunków. Wstępny cel: różnica median opóźnienia między switch/repeat <=5 ms, 95. percentyl bezwzględnego błędu względem referencji <=25 ms; progi muszą wynikać z minimalnego efektu w ms i możliwości aparatury przed akceptacją. Brak sprzętowego dowodu blokuje interpretację precyzyjnego RT.
- Ustalić dopuszczalne kombinacje urządzeń, wielkość ekranu, zasady dostępności, oraz procedurę dla osób używających technologii asystujących; nie wykluczać po cichu.
- Weryfikacja schematu, wersji i duplikatów, zapis niepełnych sesji, uprawnienia, retencja i usuwanie w zatwierdzonym środowisku. Przeprowadzić próbę odtworzenia raportu na syntetycznych danych.

## Decyzja
Udokumentować PASS/REVISE/STOP dla każdego miernika, odchylenia, uzasadnienie i podpis właściciela. Zmiany istotne dla estymandu, bodźców lub kwalifikacji wymagają nowej wersji, niezależnej próby pilotażowej i ewentualnego ponownego zatwierdzenia etycznego. Nie łączyć wersji w próbie głównej bez z góry określonej reguły.
