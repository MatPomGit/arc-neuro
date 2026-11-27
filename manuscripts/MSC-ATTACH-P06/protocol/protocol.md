# Protokół pilotażu CA 0.1.0

Uzupełnienie planu 0.2.0 przed danymi: [szczegółowy plan analizy](analysis_reporting_plan.md), [kontrakt danych](data_contract.md) i [warunki startu](precollection_checklist.md) stanowią część tego protokołu. Instrument i progi pozostają bez zmian. W szczegółach mianowników, braków, czasów i przedziałów obowiązują te uzupełnienia.

## Status i pytania badawcze

Projekt eksploracyjny dotyczący pomiaru. Nie testuje potwierdzająco H1–H5, nie służy diagnozie przywiązania i nie waliduje przyczynowego mechanizmu ARC. Badania ludzi nie zostały rozpoczęte.

Sprawdzamy: (1) rozumienie stanu i celu na dwóch współrzędnych; (2) odróżnienie dobrowolności od oddalenia; (3) rozkłady i zmienność ocen; (4) wykonalność sześciu krótkich pomiarów dziennie. Bliskość emocjonalna jest wąską operacjonalizacją, a nie pełnym pomiarem potrzeby więzi.

Przesłanka sąsiednia: Kluwer i współpracownicy (2020) badali autonomię i więź jako odrębne, współdziałające aspekty funkcjonowania relacji. Ich praca nie waliduje naszych pozycji, różnic stan–cel ani modelu ARC. Wszystkie poniższe liczebności i progi są decyzjami projektowymi do zamrożenia przed zebraniem danych danej fazy; nie pochodzą z analizy mocy.

## Faza 1: wywiady kognitywne

- Dorośli polskojęzyczni pozostający aktualnie w relacji romantycznej. Celowy dobór zróżnicowanego wieku, czasu trwania relacji i sytuacji wspólnego/oddzielnego mieszkania; opisać osiągnięte zróżnicowanie, nie twierdzić, że próba jest reprezentatywna.
- Dwie rundy po 6 nowych osób, łącznie 12. Dopuszczona jedna dodatkowa runda 6 osób, maksymalnie 18, wyłącznie po rewizji pozycji albo nierozstrzygnięciu kryteriów. Nie prowadzić nieograniczonych rund aż do uzyskania pożądanego wyniku.
- Sesja około 30–45 minut. Postępować według `instrument_pl.md`. Nie zbierać wyników par wspólnie ani ujawniać partnerowi odpowiedzi.
- Po każdej rundzie zakodować pierwsze, niewspomagane odpowiedzi; `unclear` liczy się jako niezrozumienie przy kryterium przejścia. Drugi badacz koduje niezależnie te same zanonimizowane odpowiedzi; raportować zgodność przed uzgodnieniem i zachować obie oceny. Przy braku drugiego kodera jawnie oznaczyć brak tej kontroli, nie deklarować pełnego spełnienia bramki.
- Warunek przejścia na najnowszej wersji, ocenionej przez co najmniej 6 nowych osób: dla każdej głównej pozycji co najmniej 5/6 rozróżnia stan/cel i aktualny czas odniesienia; co najmniej 5/6 rozróżnia autonomię od dystansu we wszystkich czterech winietach; wszystkie uporczywe błędy znaczenia mają rozstrzygnięcie w rejestrze.
- Zmiana po ostatniej rundzie wymaga sprawdzenia na kolejnej niezależnej grupie w granicach limitu; po wyczerpaniu limitu wynik „rewizja potrzebna”, bez przejścia do ESM. Nie usuwać trudnych uczestników z mianownika.

## Faza 2: wykonalność ESM

Osobna grupa 24 dorosłych, którzy nie brali udziału w fazie 1. Co najwyżej jedna osoba z danej pary, deklaracja bez zbierania danych partnera. To mały pilotaż pomiarowy, bez mocy do potwierdzania efektów dynamicznych lub trafności dyskryminacyjnej.

Siedem kolejnych dni, sześć powiadomień dziennie: 42 na osobę, 1008 planowanych w całej grupie. Przed startem uczestnik wybiera stałe 12-godzinne okno aktywności. Jedno losowe powiadomienie w pierwszych 90 minutach każdego z sześciu dwugodzinnych przedziałów; zachować harmonogram i ziarno generatora w prywatnym zbiorze technicznym. Takie okna dają co najmniej 30 minut odstępu. Odpowiedź do 20 minut od planowanego czasu, jedno przypomnienie po 5 minutach tylko przy braku rozpoczęcia. Bez wstecznego uzupełniania.

Zachować stałą kolejność pozycji z instrumentu podczas ESM. Instrukcja dobrowolności dostępna na ekranie; pierwsze i ponowne otwarcie pomocy rejestrowane. Pierwszy prompt dnia: sześć ocen aktualnych. Pozostałe: dziesięć pozycji, w tym cztery dotyczące okresu od poprzedniego zaplanowanego powiadomienia tego dnia. Nie wymuszać odpowiedzi ani kontaktu z partnerem. Uczestnik może zrezygnować bez konieczności uzasadnienia.

Zamknąć nabór przy 24 osobach, które rozpoczęły harmonogram. Nie zastępować osób rezygnujących po starcie i nie przedłużać badania w celu poprawy wskaźników. Osoby, które nie rozpoczęły harmonogramu, liczyć osobno w przepływie rekrutacji. Faza 2 używa jednej zamrożonej wersji; zmiana znaczenia pozycji wymaga przerwania porównywania wersji i nowego protokołu.

## Rejestracja i jakość danych

Zapisywać losowy identyfikator uczestnika, wersję instrumentu, dzień 1–7, numer promptu 1–6, planowany czas, status dostarczenia (`confirmed`/`failed`/`unknown`), rozpoczęcie i wysłanie formularza, czasy odpowiedzi na pozycje, otwarcie pomocy i wartości pozycji. Do eksportu analitycznego używać czasów względnych od startu badania; nie publikować dokładnych dat, danych urządzeń ani surowych wypowiedzi. Słownik opisuje pola pomiarowe; format techniczny formularza trzeba zweryfikować przed startem.

Pominięcie, brak strukturalny pierwszego promptu oraz błąd techniczny to różne statusy. Zera są prawidłowymi odpowiedziami. Nie imputować braków, nie usuwać odpowiedzi z powodu skrajnej wartości, małej zmienności lub szybkiego wypełnienia. Oznaczyć duplikaty i odpowiedzi po terminie; przy duplikacie zachować pierwsze ważne wysłanie, pozostałe w dzienniku. Rozpoczęte, niewysłane formularze ujmować w metrykach obciążenia i braków.

## Analizy i reguły decyzji

W raporcie pokazać licznik i mianownik każdego odsetka. Jednostką niezależną jest osoba, nie każdy prompt. Nie traktować 1008 obserwacji jako 1008 niezależnych uczestników.

| Obszar | Obliczenie | Reguła projektowa |
|---|---|---|
| Odpowiadanie | Ważne wysłania / zaplanowane prompty do chwili rezygnacji; osobno wysłania / (42 × liczba rozpoczętych osób), czyli 1008 przy pełnym naborze, wyniki każdej osoby i potwierdzone dostarczenia | Mediana osobniczego odsetka zrealizowanych pomiarów ≥75%; poniżej: poprawa harmonogramu/interfejsu |
| Czas | Mediana, IQR i P90 czasu formularza i pozycji; rozdzielić 6- i 10-pozycyjne prompty oraz formularze przerwane | Dla pełnych 10 pozycji mediana ≤90 s i P90 ≤120 s; przekroczenie: rewizja obciążenia, nie automatyczne usuwanie konstruktu |
| Braki pozycji | Braki / liczba wyświetleń danej pozycji, osobno pierwsze prompty; strukturalne braki wyłączone | >10% dla pozycji: obowiązkowe wyjaśnienie i rewizja lub uzasadniona decyzja |
| Sufit/podłoga | Dla każdej pozycji odsetek ocen ≥95 i ≤5; osobno osoby, mediana odsetków i odsetek zbiorczy | Mediana osobniczego udziału w którymkolwiek końcu >50%: flaga ograniczenia zakresu |
| Zmienność | Odchylenie standardowe wewnątrz każdej osoby z ≥10 ważnymi ocenami; liczba osób poniżej tego minimum; rozkład SD | Mediana SD <5 punktów: flaga małej użyteczności dynamicznej, nie dowód stałej potrzeby |
| Odrębność | Wykresy C_state–A_state oraz A_state–W_solitude/X_distance; korelacje wewnątrzosobniczo centrowane i między średnimi osobniczymi osobno | Brak sztywnego progu potwierdzającego trafność. Wysoka korelacja i mylenie pojęć uzasadniają rewizję; niska korelacja nie dowodzi trafności |

Dla SD i korelacji raportować rozkłady i liczbę dostępnych osób; korelacji nie liczyć przy zerowej wariancji. Dla median osobniczych wskaźników wykonalności raportować 95% przedziały bootstrapowe, resamplując całe osoby (2000 losowań, ziarno 20260930), nie prompty; ograniczenia przy <10 osobach i degeneracji określa plan analizy. Żaden wskaźnik pilotażu nie stanowi testu H1/H2, a korelacje z działaniem są jedynie opisowe.

**Decyzje:**

1. Niespełnione rozumienie: rewizja pytań przed ESM.
2. Niespełnione wskaźniki wykonalności: rewizja procesu i powtórny pilotaż; nie przejście automatyczne do badania potwierdzającego.
3. Stały/sufitowy A_target: zachować wynik, rozważyć w nowym projekcie model stanu autonomii/presji lub jednostronnego niezaspokojenia zamiast dynamicznego celu. Nie dopasowywać skali tak, aby wymusić wariancję.
4. Dobre rozumienie i wykonalność: zamrozić wersję do dalszej walidacji i kalibracji projektu, nie ogłaszać zwalidowanej skali.
5. Dane nierozstrzygające: jawnie pozostawić status kandydacki. Pozycje i konstrukt można odrzucić z bieżącej operacjonalizacji bez twierdzenia, że potrzeba autonomii nie istnieje.

## Formalizacja do późniejszej kalibracji

Dla q ∈ {C,A}: e_q(t) = target_q(t) − state_q(t). Nie sumować e_C i e_A do jednego „bezpieczeństwa”, nie obliczać alfa Cronbacha dla par stan–cel lub obu potrzeb jako jednej skali.

Przyszły model kanału k może porównać osobne ścieżki:

`action_k(t+1) = baseline + b_Cs state_C_wp(t) + b_Ct target_C_wp(t) + b_As state_A_wp(t) + b_At target_A_wp(t) + error`.

Model dwóch różnic nakłada ograniczenia `b_Ct = -b_Cs` i `b_At = -b_As`. `wp` oznacza odchylenie od średniej osoby wyliczanej wyłącznie na zbiorze treningowym w przyszłej walidacji. Baseline musi uwzględniać kontekst, historię działania i efekty międzyosobnicze. Nie wymuszać znaków wpływu autonomii na zbliżenie lub dystans.

To kandydackie równania do nowej symulacji, nie analiza potwierdzająca niniejszego pilotażu. Alternatywy przy suficie celu: sam stan A, osobna presja P albo `max(A_target − A_state, 0)`. Ich wybór po pilotażu jest rozwojowy; porównanie wymaga później odrębnych danych, jawnych progów, pomiaru błędu, liczebności i planu walidacji. Dane pilotażu nie będą finalnym holdoutem tej walidacji. Współrzędne C/A nie zastępują osobowych L/U ani nie oznaczają nowej wersji rdzenia ARC.

## Zamrożenie i raport

Przed każdą fazą wpisać datę, wersję instrumentu, parametry projektu i osobę odpowiedzialną do prywatnego rejestru. Po fazie zapisać każdą decyzję `retain`/`revise`/`drop`/`inconclusive`, jej kryterium, licznik/mianownik, uzasadnienie i nową wersję. Surowe dane oraz decyzje muszą pozostać rozdzielone. Przy nowej wersji nie nadpisywać wcześniejszych ocen.

Raport końcowy zawiera przepływ uczestników, wersje i zmiany, zgodność koderów, wyniki wszystkich kryteriów, braki i błędy techniczne, negatywne/niejednoznaczne wyniki, zakres możliwych wniosków oraz decyzję o dalszych pracach. Nie zastępować go samym wynikiem „zaliczono”.

## Źródło sąsiednie

Kluwer, E. S., Karremans, J. C., Riedijk, L., & Knee, C. R. (2020). Autonomy in relatedness: How need fulfillment interacts in close relationships. *Personality and Social Psychology Bulletin, 46*(4), 603–616. https://doi.org/10.1177/0146167219867964

Metadane i zakres sprawdzono w [PubMed](https://pubmed.ncbi.nlm.nih.gov/31390934/) i [tekście pracy](https://pmc.ncbi.nlm.nih.gov/articles/PMC7057354/). Pozycje i progi tego protokołu są propozycjami ARC, a nie adaptacją zwalidowaną przez tę publikację.

