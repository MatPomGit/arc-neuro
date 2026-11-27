# Plan analizy i wartości informacyjnej pilotażu

Status: plan przed danymi, wersja dokumentu 0.1.0. Instrument pozostaje CA 0.1.0. Ten plan doprecyzowuje `protocol.md`; progi liczbowe nadal pochodzą z `design_config.json`. Nie zmienia H1 ani rdzenia ARC.

## Główny cel niezależny od teorii

Pilotaż ma odpowiedzieć, **czy i w jakich warunkach można mierzyć rozróżnialne stany i cele bliskości oraz dobrowolności w codziennym życiu**. Jego wartością jest oszacowanie błędów rozumienia, obciążenia, braków, zakresu i zmienności pomiaru. Nie ma w nim głównego testu „czy ARC jest prawdziwy”. Nie obiecujemy, że każdy zbiór pozwoli rozstrzygnąć teorię lub uzyskać publikację.

## Rejestr wyników obowiązkowych

Każdy wiersz jest raportowany, nawet jeśli nie daje oczekiwanego wyniku. Nie wyznacza się zwycięzcy na podstawie najmniejszego p.

| ID | Wynik i populacja analityczna | Obowiązkowy produkt |
|---|---|---|
| CA-Q1 | Pierwsze niewspomagane odpowiedzi każdej osoby w każdej rundzie, według wersji | Zrozumienie czterech pozycji i czterech winiet, licznik/mianownik, `unclear` oraz zgodność koderów przed uzgodnieniem |
| CA-F1 | Wszyscy, którzy rozpoczęli harmonogram, łącznie z rezygnującymi i osobami bez odpowiedzi | Przepływ rekrutacji, dostarczenia, realizacja promptów i rezygnacje |
| CA-F2 | Każda rozpoczęta próba odpowiedzi | Czas formularza/pozycji, formularze przerwane i liczba nieobserwowanych czasów; osobno prompty 6- i 10-pozycyjne |
| CA-M1 | Wszystkie wyświetlone pozycje, również w przerwanych formularzach | Braki według pozycji, wersji i dnia; bez mieszania braku strukturalnego i technicznego |
| CA-M2 | Ważne wartości pozycji | Sufit/podłoga, rozkład, SD wewnątrz osoby z ≥10 ocenami, liczba osób poniżej tego minimum |
| CA-D1 | Osoby z parami ważnych ocen i niezerową wariancją | Opisowa odrębność współrzędnych, wykresy i korelacje; brak dowodu trafności z samej niskiej korelacji |

Nie tworzyć jednego łącznego wyniku „sukcesu badania”, który ukrywa niepowodzenie którejś domeny. Spełnienie flag wykonalności nie jest dowodem trafności psychometrycznej.

## Mianowniki i niepewność

- Realizacja do rezygnacji: ważne wysłania / prompty zaplanowane do chwili rezygnacji, także niedostarczone. Oddzielnie realizacja wśród potwierdzonych dostarczeń; `unknown` nie oznacza `confirmed`.
- Realizacja pełnego planu: ważne wysłania / (42 × liczba osób, które rozpoczęły harmonogram). Przy pełnym naborze mianownik wynosi 1008. Przy wcześniejszym zakończeniu nie przedstawiać 1008 jako liczby promptów rzeczywiście zaplanowanych dla rozpoczętych uczestników. Podać także nominalny cel 1008. Przy zerowym mianowniku wynik to `NA`, nigdy 0% ani 100%.
- Formularz „ważnie wysłany” może mieć pominięte pytania. Realizacja formularzy i kompletność pozycji są różnymi wynikami. Nie karać uczestnika wykluczeniem za małą liczbę odpowiedzi.
- Czas: surowy czas od otwarcia do wysłania; osobno aktywny czas, jeśli interfejs umie go wiarygodnie rejestrować. Nie odcinać długich czasów po obejrzeniu rozkładu. Przerwane formularze mają czas obserwowany do przerwania, nie pełny czas ukończenia.
- SD próbne (`ddof=1`), kwantyle z interpolacją liniową między uporządkowanymi wartościami. W podsumowaniach pomiaru pokazać osobno rozkład wyników osobniczych i wyniki wszystkich obserwacji, aby osoby często odpowiadające nie ukryły pozostałych.
- Przedziały 95% dla median osobniczych wskaźników wykonalności: bootstrap całych osób, 2000 losowań, ziarno 20260930; metoda percentylowa. To przybliżona niepewność w małej próbie, nie gwarancja pokrycia. Przy <10 osobach uprawnionych do danego wskaźnika raportować punkty i zakres, bez przedziału bootstrapowego i bez decyzji o przejściu do kolejnego etapu na podstawie tej metryki. Degenerację przedziału jawnie oznaczyć. Wyniki rund kognitywnych podawać jako zliczenia, bez pozornej precyzji inferencyjnej.
- Flagi z protokołu odnoszą się do oszacowań punktowych. Nie interpretować minimalnego przekroczenia progu jako ostrej granicy psychologicznej; pokazać też niepewność. Zmiana progu po danych jest odstępstwem, nie nowym „wcześniej ustalonym” kryterium.

## Macierz interpretacji przed danymi

| Możliwy wynik | Co rzeczywiście wnosi | Decyzja i zakaz nadinterpretacji |
|---|---|---|
| Uczestnicy mylą stan i cel | Wykryta wada operacjonalizacji | Rewizja pozycji; nie odrzucenie potrzeby ani całej teorii |
| Autonomia mylona z oddaleniem | Brak zrozumiałego rozróżnienia w tym narzędziu | Poprawa definicji/pomiaru albo rezygnacja z tej współrzędnej w bieżącej wersji |
| Cel A niemal zawsze maksymalny | Ograniczona informacyjność dynamicznego celu A | W nowym projekcie porównać stan, presję lub jednostronne niezaspokojenie; nie „naprawiać” odpowiedzi |
| Dobre rozumienie, mała zmienność | Brak dostatecznej informacji dla dynamiki w tym czasie i próbie | Zmienić projekt próbkowania prospektywnie lub uprościć model; nie dowód stałości potrzeby u ludzi |
| Dużo niedostarczonych promptów | Ograniczenie infrastruktury | Naprawić system; nie przypisywać awarii uczestnikom |
| Prompty docierają, odpowiedzi rzadkie/długie | Ograniczenie obciążenia lub kontekstu | Zmniejszyć obciążenie w kolejnej wersji; raportować attrition i ograniczenia selekcji |
| Rozbieżność nie wiąże się z działaniem | Co najwyżej opisowy wynik tej próby; możliwa nieprecyzyjność | Brak podstaw do potwierdzenia lub obalenia H1 w CA; nie dobierać opóźnień i podgrup aż do istotności |
| Związek jest dodatni | Kandydat do niezależnej próby, nie walidacja mechanizmu | Zaplanować odrębną kalibrację i nowe dane |
| Dane zbyt niepełne lub uszkodzone | Udokumentowana granica wykonalności lub utraty danych | Raport techniczny i zakres utraty; żadnych wyników psychologicznych z nieodtwarzalnego zbioru |

„Nieistotny” nie oznacza „równoważny zeru”. CA nie ma skalibrowanego marginesu równoważności dla efektu teorii. Nie zapożyczać progów H1 z innej skali i projektu.

## Granica między planem a eksploracją

Dla opisowych korelacji CA-D1: C_state–A_state, A_state–W_solitude i A_state–X_distance. Korelacje między średnimi osobniczymi liczyć dla osób z ≥10 wspólnymi parami; korelacje po centrowaniu osobniczym na tych samych parach, z usunięciem tylko osób o zerowej wariancji danej pary. Zawsze podać liczbę osób i par. Te analizy są opisowe, nie potwierdzające.

Wszelkie dodatkowe podgrupy, nieliniowości, opóźnienia, interakcje i zmienione pozycje trafią do osobnego rejestru eksploracji z datą i informacją, jakie dane były już widoczne. Raport obejmie wszystkie wykonane analizy, także niesprzyjające modelowi. Nie używać tych samych danych do odkrycia, dostrojenia i końcowego potwierdzenia zmienionej teorii. Nie przeznaczać części małego CA na pozornie mocny końcowy test mechanizmu; niezależna walidacja wymaga nowych danych.

## Produkty niezależne od kierunku wyniku

1. Jeden pełny raport pomiarowo-metodologiczny według `report_template.md`, także przy zatrzymaniu po wywiadach. Niewykonane fazy oznaczyć jako niewykonane.
2. Wersjonowany instrument i historia powodów zachowania/rewizji/odrzucenia pozycji.
3. Zagregowane statystyki zakresów, zmienności, braków i obciążenia do projektowania następnego badania; nie estymować docelowej mocy wyłącznie z niestabilnego małego efektu CA.
4. Odtwarzalny kod analizy, syntetyczne przykłady i słownik eksportu. Surowe dane ludzi udostępniać tylko w zakresie faktycznie uzyskanych zgód i oceny prywatności, nie automatycznie publicznie.
5. Kandydat na artykuł metodologiczny o pomiarze i wykonalności; publikowalność zależy od jakości danych i wkładu. Nie gwarantować publikacji i nie dzielić jednego małego zbioru na serię pozornie niezależnych testów.

## Uzasadnienie metodologiczne

[COS: prerejestracja](https://www.cos.io/initiatives/prereg) uzasadnia rozróżnianie analiz zaplanowanych i eksploracyjnych. [Eldridge i in., BMJ 2016, doi:10.1136/bmj.i5239](https://www.bmj.com/content/355/bmj.i5239) omawiają cele wykonalności i kryteria przejścia w pilotażach randomizowanych. CA nie jest RCT: wykorzystujemy tę ogólną zasadę planowania, nie deklarujemy zgodności z checklistą dla RCT. Konkretne miary i progi CA pozostają naszymi decyzjami projektu.
