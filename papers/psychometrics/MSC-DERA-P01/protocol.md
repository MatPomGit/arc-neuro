# Protokół walidacji DERA-HRI

Wersja 1.0.0, 27.11.2026. Właściciel naukowy i autor Mateusz Pomianek. Stan `CANDIDATE_VALIDATION_DATA_REQUIRED`.

## Proweniencja i pilotaż

Katalog programu identyfikuje publiczny szkic P01 i powiązanie z INS-DERA-I01. Przed udostępnieniem narzędzia zatwierdzić wersję, język, autorstwo, uprawnienia, pełną treść, etykiety kategorii, instrukcję, sposób obliczania wyników i mapę pozycji. Zamrozić manifest z sumą SHA-256. Brak źródła blokuje przypisywanie narzędziu określonych wymiarów, liczby pozycji i klucza.

Ocenę treści przeprowadzi panel 5–8 osób z kompetencjami w HRI, psychometrii i psychologii afektu. Każdą pozycję ocenią niezależnie na czterech poziomach adekwatności, dopasowania do konstruktu i zrozumiałości. Raport obejmie rozkład decyzji, I-CVI, uwagi oraz uzasadnienie poprawek. Przeprowadzić 8–12 wywiadów poznawczych w dwóch rundach. Sprawdzić znaczenie zwrotów dotyczących relacji, różnicę między reakcją w trakcie zadania a oceną wyglądu oraz przyczyny wybierania skrajnych kategorii.

## Akwizycja

Dorośli polskojęzyczni, po zgodzie, wykonują standaryzowane zadanie z humanoidem. Rejestr obejmuje wersję scenariusza, robota, tryb sterowania, odstępstwa, wcześniejsze doświadczenie z robotami i czas od interakcji do kwestionariusza. Wideo i kontakt bezpośredni wymagają jawnego rozróżnienia i odrębnej oceny inwariancji. Materiał wideo może służyć do oceny rozumienia bodźców, ale nie zastępuje próby walidacyjnej dla uczestników rzeczywistej interakcji.

Oddzielić próbę EFA i niezależnie rekrutowaną próbę CFA. Osoby z wywiadów poznawczych i osoby powracające identyfikuje pseudonim. Duplikaty zachowują pierwszy kwalifikujący się komplet. Odmowa, awaria procedury i dane brakujące dostają odrębne kody. Krótkiego czasu odpowiedzi ani nietypowego wyniku nie używać samodzielnie do wykluczeń. Przed analizą określić dopuszczalny odsetek braków na osobę i pozycję, a następnie raportować pełne przypadki oraz analizę wrażliwości na mechanizm braków.

## Analiza

EFA obejmuje analizę równoległą zachowującą progi marginalne, rotację ukośną, ocenę interpretowalności i zależności lokalnej. Z góry ustalić regułę wyboru, uwzględniając ładunki poniżej 0,40, ładunki krzyżowe i pokrycie treści. Wysokie współczynniki nie uzasadniają automatycznego usuwania merytorycznie istotnych pozycji. Próbę CFA otworzyć dopiero po zapisie decyzji EFA i wersji banku. W CFA użyć estymatora porządkowego, raportować wskaźniki dopasowania, przedziały i reszty. Punkty odniesienia dopasowania wymagają kalibracji symulacyjnej dla konkretnego modelu i nie zastępują diagnozy reszt. Zmiany po CFA oznaczać jako eksploracyjne i weryfikować na kolejnej próbie.

Na etapie CFA porównać model zamrożony z jednoczynnikowym oraz alternatywą merytoryczną, jeśli jest identyfikowalna. Trafność zbieżną i różnicową oceniać przez zdefiniowane przed analizą kontrasty korelacji latentnych i 95% przedziały. Godspeed i RoSAS stosować w wersjach o sprawdzonej dostępności i zgodności językowej. Zgodność progów oraz ładunków sprawdzać przy zdefiniowanej identyfikacji i odpowiedniej liczebności grup. Skorygować wielokrotność kontrastów wtórnych metodą Holma. Wynik całkowity wymaga dowodów na jego interpretowalność.

Po pilotażu przeprowadzić Monte Carlo właściwego estymatora. Skrzyżować liczebność z ładunkami, korelacjami czynników, progami, brakami oraz niezrównoważonymi grupami. Docelowe progi projektu obejmują co najmniej 95% poprawnych dopasowań, raport pokrycia i obciążenia z błędem Monte Carlo oraz wcześniej uzgodnioną szerokość przedziału dla kluczowych ładunków. Przy bieżącej nieznajomości struktury wykonano wyłącznie planistyczne oszacowanie ryzyka rzadkich kategorii.

## Dane i warunki rozpoczęcia

Minimalna tabela prób obejmuje participant_id, cohort, scenario_id, instrument_version, item_id, category, administration_order, protocol_deviation i missing_reason. Informację kontaktową i klucz pseudonimów przechowywać osobno od danych prób. Repozytorium publiczne zachowuje metody i symulacje. Decyzję etyczną, plan retencji oraz prerejestrację OSF ustalić przed zebraniem próby głównej. Projekt ma status prospektywny.
