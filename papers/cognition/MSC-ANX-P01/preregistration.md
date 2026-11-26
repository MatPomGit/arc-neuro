# MSC-ANX-P01: projekt prerejestracji, v0.1.0

Scientific owner i autor: Mateusz Pomianek. Status: PROSPECTIVE / IDEA_REVIEW, projekt niezamrożony, 2026-11-26. Przeznaczony do adaptacji do formularza rejestracji po pilotażu i zatwierdzeniu etycznym. Nie złożono rejestracji, nie przypisano DOI.

## Pytanie i zakres
Czy w populacji dorosłych nasilenie objawów lękowych wiąże się z kosztem przełączania reguł i preferencjami decyzji pod ryzykiem i niejednoznacznością? Badanie przekrojowe, obserwacyjne z zadaniami behawioralnymi; randomizacja dotyczy kolejności i bodźców, nie lęku. Brak identyfikacji przyczynowej.

## Hipotezy i punkty końcowe
- H1, główna: dodatni współczynnik GAD-7/5 w OLS kosztu przełączania (różnica median poprawnych RT switch minus repeat, ms).
- H2, drugorzędowa: ujemny warunkowy log-OR wyboru opcji bardziej zmiennej na 5 punktów GAD-7, przy kontroli różnicy EV i wariancji.
- H3, drugorzędowa: ujemny warunkowy log-OR wyboru opcji niejednoznacznej na 5 punktów GAD-7, przy kontroli nominalnej różnicy wypłat i szerokości przedziału. Nie przypisujemy znanego EV niejednoznacznej opcji.
- H4, eksploracyjna: H2/H3 z dodatkowym indywidualnym kosztem przełączania; nie interpretować jako mediacji.

Testy dwustronne, H1 alfa 0,05, H2/H3 jedna rodzina Holma 0,05, H4 bez wnioskowania konfirmacyjnego. Kierunek przeciwny do przewidywanego nie potwierdza hipotezy nawet przy istotnym wyniku. Raportować oszacowania, CI, surowe i skorygowane p. Wyniki zerowe zachować.

## Próba i zatrzymanie
Pełnoletnie osoby rozumiejące język polski, z komputerem i fizyczną klawiaturą, dobrowolny udział. Nie wymaga się rozpoznania klinicznego i nie selekcjonuje według GAD-7. Wstępnie pilotaż 40 osób (dopuszczalny zakres 30–50 w prospekcie, docelowy limit pilotażu zatwierdzić przed startem); odrębna próba, niewłączana do analizy głównej. Wstępnie 355 analizowalnych obserwacji H1, 444 rekrutowanych, r częściowe obserwowane 0,15, alfa 0,05, moc 0,80, 8 stopni swobody współzmiennych. Finalne N ustalić po ocenie jakości, wariancji i braków oraz kalibracji modeli; nie używać pilotażowego związku GAD-7 z wynikiem do wyboru efektu. W finalnej rejestracji zapisać maksymalną liczbę przyjętych sesji i datę zamknięcia; zatrzymanie według wcześniejszego z tych limitów, bez podglądu efektów. Liczbę kompletnych przypadków traktować jako cel planistyczny, nie regułę opcjonalnego zatrzymania. Rekrutacja bez wynagrodzeń jest propozycją, nie zatwierdzonym warunkiem.

## Plan procedury
Informacja o badaniu, zgoda, kontrola warunków technicznych i rozumienia, GAD-7 i zatwierdzona skala depresyjności oraz wiek i sen. Dwa zadania z równoważeniem kolejności, instrukcje i trening bez zapisu do wyniku właściwego. Zadanie klasyfikacji: 24 próby treningu, próg 18/24, jedna powtórka; 48 prób jednorodnych i 192 mieszane; 94 switch, 94 repeat, cztery inicjalne. Sygnał 300 ms, deadline 2000 ms, ITI 500 ms. Zadania decyzyjne: 48 ryzyka i 48 niejednoznaczności, kontrola zrozumienia przed decyzjami, brak rzeczywistej wypłaty i limitu czasu odpowiedzi. Kolejność risk–ambiguity jest równoważona niezależnie od kolejności klasyfikacja–decyzje (wersja bodźców 0.4.2); uwzględnia się ją w modelach wyboru. Dwa niezaliczone treningi lub quizy wykluczają tylko odpowiednią grupę zadań. Zakończenie, debriefing i informacja o pomocy. Szczegóły i proponowane bramki: [pilot-protocol.md](pilot-protocol.md).

## Analiza
[Plan analiz](analysis-plan.md) określa jednostki, modele, braki, QA, kontrolę błędów oraz interpretację. Kod referencyjny jest wyłącznie syntetyczny; finalna akwizycja i analiza wymagają wersji kanonicznej i przeglądu.

## Informacja o danych i odstępstwach
Dane zdrowotne i zachowanie w zadaniu są przetwarzane tylko w zatwierdzonym środowisku; repozytorium publiczne zawiera kod demonstracyjny i prospektywne materiały. Ograniczenia udostępniania, retencja, zgoda i zasady wycofania w [ethics-data.md](ethics-data.md). Rejestr odstępstw musi zawierać czas, decyzję, powód, dostęp do danych i wpływ na estymand; zmiany po zamrożeniu oznaczają analizy eksploracyjne, jeśli naruszają pierwotny plan. Nie nadpisywać pierwotnej rejestracji.

## Bramki zamrożenia
1. Właściciel zatwierdza kanoniczne repozytorium, wersję protokołu, hipotezy, licencje i polskie skale.
2. Zatwierdzenie etyczne i ochrony danych przed jakąkolwiek rekrutacją, również do pilotażu.
3. Walidacja sprzętowa timing, E2E, bezpieczeństwo, dostępność, separacja treningu i danych właściwych.
4. Pilotaż, jawna ocena bramek i decyzja o powtórzeniu.
5. Kalibracja H1/H2/H3, finalne N, reguła zatrzymania, pełne środowisko z lockfile i SHA.
6. Zapis treści finalnej rejestracji i potwierdzony identyfikator z wybranego rejestru przed próbą główną. Dostępność platformy i jej aktualny formularz wymagają osobnego sprawdzenia; ten plik nie jest dowodem rejestracji.
