# Projekt prerejestracji i zarządzania danymi

MSC-CR-P12 · 1.0.0 · 27.11.2026 · Mateusz Pomianek. Projekt do pilotażu. Rejestracja OSF i decyzja etyczna pozostają do uzyskania przed badaniem głównym.

## Próba i harmonogram

Dorośli w wieku co najmniej 18 lat, czytający po polsku, z dostępem do przeglądarki. Rekrutacja otwarta w internecie, informacja o fikcyjnych rekomendacjach, zgoda przed pretestem. Wiedza mierzona przed randomizacją po czterech osobnych pozycjach na dziedzinę, z opcją „nie wiem”. Te pytania mają dotyczyć wiedzy, a nie przedstawiać scenariuszy ani uczyć reguł. Pokazać rozkład wykształcenia i częstotliwości korzystania z AI. Używać neutralnej informacji o „ocenie sposobu pracy z rekomendacjami”. Po ostatniej wizycie przekazać wyjaśnienie manipulacji.

T0 i T1 podczas pierwszej wizyty, T2 po 14 dniach (dopuszczalne dni 12–16). T0/T1/T2 po 16 nowych pozycji na domenę, po osiem porad każdego rodzaju. Formy A/B/C rozdzielić sześcioma permutacjami. Serwer losuje po T0 w blokach o zmiennej długości, stratyfikując według kolejności form. Wersja rady odwrócona dla połowy uczestników w obrębie każdej formy, grupy i pozycji. Wstępna kolejność odpowiedzi i kolejność prób losowane osobno. Pretest obejmuje wszystkie dziedziny bez informacji zwrotnej, więc transfer dotyczy domen bez treningu, lecz z ekspozycją pomiarową. Hipotezy nie dotyczą transferu do domen nigdy wcześniej oglądanych.

Trening i kontrola po ok. 12 minut i osiem osobnych ćwiczeń. Trening pokazuje poprawne i błędne rekomendacje, ćwiczy najpierw samodzielny wybór, potem sprawdzenie warunków, kryterium i uzasadnienia. Stosuje kontrprzykłady oraz informację, dlaczego warto przyjąć poradę poprawną. Kontrola ćwiczy odczyt jawnej etykiety lub jednostki z tej samej karty i dostaje równoważną długością informację zwrotną do tego zadania, bez instrukcji weryfikacyjnych. Oceniający klucze i osoby analizujące zaślepione względem etykiet grup do wykonania zamrożonego skryptu.

## Materiały i pilotaż

Bank kandydacki obejmuje mobilność, ekologię i wyposażenie oraz po trzy zestawy po 16 pozycji. Dla każdego scenariusza zachowano jeden klucz i symetryczny szablon rady. Scenariusze są fikcyjne i pozbawione stawki. W każdej domenie skrzyżować format z rodziną błędu, aby oszacować wpływ zmiany prezentacji niezależnie od zmiany tematyki. Obecny bank parametryczny pozwala zweryfikować logikę i prototyp. Przed badaniem głównym trzeba rozszerzyć zróżnicowanie treści, przygotować osobną pulę ćwiczeń i pytań wiedzy, zwłaszcza pozycje dotyczące podstawy porównania i niepełnego dowodu, oraz sprawdzić podobieństwo form. Wynik z obecnych równoległych reguł uzasadnia wąski transfer międzydziedzinowy.

Dwóch niezależnych recenzentów ocenia jednoznaczność klucza, niezbędność dowodu, dziedzinę, rodzinę błędu i dopasowanie rady do klucza. Rozbieżności rozstrzyga trzeci recenzent. W oddzielnym panelu bez dostępu do klucza uczestnicy oceniają wiarygodność stylistyczną i naturalność na skali 1–7. Kandydat do banku wymaga uzgodnionego klucza i średniej różnicy wariantów w wiarygodności stylistycznej do 0,5 pkt, z 90% przedziałem w obrębie ±0,75 pkt na poziomie pulek. Ujednolicić długość, pewność tonu, źródło i interpunkcję. Wiarygodność merytoryczna może zasadnie różnić się po zapoznaniu z dowodem.

Wywiady poznawcze z 8–12 osobami sprawdzą interpretację poleceń i pewności. Oddzielny pilotaż N=60–90 służy ocenie wykonalności, rozkładów trafności, rzetelności domen i utraty w T2. Projekty form powinny mieć zbliżone średnie i 90% przedziały różnicy d′ wewnątrz ±0,30, w razie braku precyzji rozszerzyć kalibrację. Pozycję z wyjściową skutecznością decyzji poniżej 0,30 albo powyżej 0,90 poprawić i ponownie ocenić. Wznowienie sesji i eksport zweryfikować na danych syntetycznych. Pilotażu nie włączać do próby głównej.

## Analiza i decyzje

ITT według przydziału, z wykorzystaniem dostępnych prób. Odrzucić rekordy testowe, wpisy poza kryteriami zgody i wieku, techniczne duplikaty (zostawić pierwszą ważną randomizację) i odwiedziny poza oknem T2 (oznaczyć brak wyniku). Krótki czas, nieuwaga lub niski wynik nie usuwają osoby z ITT. Analiza per protocol po ukończeniu przynajmniej 6/8 ćwiczeń pozostaje pomocnicza. Raport przepływu uczestników z powodami, czasy, brakujące próby i wskaźniki powrotu w grupach.

Hierarchiczny probit z efektami uczestnika i scenariusza. Model bazowy opisuje równanie w manuskrypcie. Równoważenie form w analizie przez efekt stały formy; efekty losowe scenariuszy odpowiadają odchyleniom w obrębie formy. Dodatkowa standaryzacja przy oszacowaniu prawdopodobieństw z równymi wagami domen oraz wspólnym empirycznym rozkładem wiedzy. Analiza w Pythonie. Plan estymacji MCMC z czterema łańcuchami, regularizującymi rozkładami normalnymi dla efektów stałych oraz półnormalnymi dla odchyleń losowych. Rozbieżności HMC, R-hat ponad 1,01 albo ESS poniżej 400 dla kontrastu wstrzymują wniosek. Raportować medianę, 95% przedział i obie stopy decyzyjne. Jedyny test pierwszorzędowy dotyczy H1. H2 i H3 są drugorzędowe, z korektą Holma dla trzech kontrastów (efekt bliski, gradient bezpośredni, utrzymanie akceptacji). H4 i miary pewności raportować jako wsparcie modelu i eksplorację. Brier to średni kwadrat różnicy pomiędzy prognozowaną pewnością a poprawnością; model kalibracji opisuje przesunięcie i nachylenie logitu, z ograniczeniem prognoz do [0,005; 0,995] i grupowaniem według osoby. RAIR i RSR używają tylko prób, w których AI i uczestnik początkowo wskazali różne opcje. Każdy mianownik raportować osobno.

Podstawowe wnioskowanie zakłada MAR warunkowo względem grupy, bazowej trafności, wiedzy i dostępnego wyniku T1. W analizie wrażliwości zastosować model mieszaniny wzorców i przesunięcia d′ brakujących w T2 od −0,50 do +0,50 niezależnie według ramienia, z raportem progu zmiany wniosku. Rozkłady braku wyników opisać w obu ramionach. Symulacja planistyczna jest przybliżeniem opartym o zmianę indywidualnego d′ i test Welcha; zasymulowane wskaźniki nie są potwierdzoną mocą estymatora wielopoziomowego.

## Słownik danych i retencja

| Pole | Typ i dziedzina | Znaczenie |
| --- | --- | --- |
| participant_id | losowy pseudonim | Klucz wizyt, oddzielny od adresu kontaktowego |
| arm | training/control | Losowany przydział |
| phase | T0/T1/T2/training | Fala lub interwencja |
| item_id, form, domain, family | kod katalogowy | Wersja bodźca i pozycja w planie |
| correct_option, ai_option, initial, final | A/B | Klucz, rada i oba wybory |
| accepted | 0/1/brak | Deklarowana akceptacja |
| confidence | 0,50–1,00/brak | Pewność trafności decyzji o akceptacji |
| knowledge_score | 0–4/brak na domenę | Pomiar przed przydziałem |
| rt_ms, trial_order | liczba całkowita | Czas i porządek próby |
| window_status, missing_reason | kod | Odchylenie od terminu i powód braku, jeśli znany |
| protocol_version, bank_hash | tekst | Wersja procedury i hash pliku banku |

Zgody i listę kontaktową przechowywać oddzielnie na zatwierdzonej infrastrukturze instytucjonalnej. Baza prób zawiera pseudonim, bez IP, surowych logów przeglądarki i danych kontaktowych. Ograniczyć role zespołu, szyfrować transmisję i kopie, ustalić tryb wycofania i retencję z administratorem oraz komisją przed startem. Usuń mapę kontaktową po zamknięciu okna wycofania zgodnie z uzgodnioną procedurą. Publiczne repozytorium przechowuje wyłącznie bodźce fikcyjne i dane syntetyczne. Udostępnienie zagregowanych danych wymaga oceny ryzyka ponownej identyfikacji.

## Zamrożenie i wdrożenie

OSF przed pierwszą randomizacją badania głównego. Zarejestrować hipotezy, estymand, regułę zatrzymania rekrutacji, wersję i hash banku, warunki analizy braków, skrypt mocy właściwego estymatora, kolejność analizy oraz status etyczny. Zapisać odstępstwa osobno, z datą i uzasadnieniem. JATOS obsługuje własny HTML/JS i integrację z jsPsych. Bezpłatny publiczny hosting wymaga niezależnego potwierdzenia zgodności z uzgodnionym planem danych; preferowana jest zatwierdzona instancja instytucjonalna. Prototyp lokalny uruchamia się przez `python materials.py > items.json`, a następnie `python -m http.server 8000` w katalogu projektu. Nie ma serwerowej randomizacji, uwierzytelniania powrotu ani zapisu uczestników.
