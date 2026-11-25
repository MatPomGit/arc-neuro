# Projekt prerejestracji MSC-CR-P06

Wersja 0.1.0, 2026-11-24. Właściciel naukowy: Mateusz Pomianek. Status: DRAFT_NOT_REGISTERED / PROSPECTIVE. Nie rozpoczęto rekrutacji głównej, nie zgłoszono tej prerejestracji, nie nadano DOI. Dokument wymaga zamrożenia po pilotażu i przed dostępem do danych głównych.

## Pytanie i hipotezy

Czy krótka edukacja o ograniczeniach AI i weryfikacji informacji poprawia niezależny osąd w nowych zadaniach bez AI w porównaniu z aktywną kontrolą? H1: większa trafność bezpośrednio po lekcji. H2: większa trafność po tygodniu. H3: mniejszy wynik Briera. H4: większa średnia ocena jakości argumentacji. H1 jest jedyną hipotezą pierwszorzędową. H2–H4 stanowią rodzinę drugorzędową. Pozostałe porównania, w tym wiedza i doświadczenie AI, są eksploracyjne. Nie uznawać samych deklaracji za dowód transferu.

## Projekt i populacja

Randomizowany eksperyment online, dwa ramiona 1:1, pełnoletni uczestnicy posługujący się językiem polskim. T0 przed przydziałem, T1 bezpośrednio po około 15-minutowej lekcji, T2 po 7 dniach (okno 6–8 dni). Udział dobrowolny, bez wpływu na oceny akademickie. Interwencja i kontrola mają po 10 ekranów i 4 ćwiczenia; finalna równoważność obciążenia wymaga pilotażu. Wykluczenia przed randomizacją: wiek poniżej 18 lat, brak zgody, brak ukończenia pretestu, stwierdzony duplikat według zatwierdzonej reguły. Po przydziale nie wykluczać na podstawie wyniku, tempa ani deklarowanej zgodności z instrukcją. Wycofanie zgody zgodnie z zaakceptowaną informacją dla uczestnika.

## Alokacja i pomiar

Przed pretestem losować formę T0; przydział ramienia ujawniać dopiero po jego ukończeniu. Proponowana warstwa doświadczenia AI: użycie narzędzi generatywnych co najmniej raz w tygodniu w ostatnich 30 dniach vs rzadziej; próg wymaga potwierdzenia przed zamrożeniem. Losowanie centralne z ukryciem alokacji; sześć sekwencji form równoważyć w obrębie ramion i warstw, warunkowo na formie T0. Szczegółowy algorytm i rozmiary bloków zatwierdzić przed rekrutacją. Sędziowie uzasadnień nie znają ramienia ani punktu pomiaru. Każda forma ma 24 pozycje, 6 z uzasadnieniem. Publiczny bank demonstracyjny nie jest zamrożonym testem głównym; finalne bodźce i klucz wymagają kontrolowanego dostępu, identyfikatorów wersji i niezależnej walidacji.

## Liczebność i zakończenie rekrutacji

Roboczy efekt d=0,35, alfa=0,05, moc=0,80, przewidywane 15% braków. Konserwatywny scenariusz bez korekty korelacyjnej: N=304. Alternatywy 276/230/156 wynikają wyłącznie z założonych korelacji 0,3/0,5/0,7. Nie wyznaczono ostatecznego N; przed zamrożeniem uzasadnić minimalny efekt w punktach procentowych i uwzględnić pilotaż oraz symulacje. Przyjąć stały cel liczby randomizowanych, bez opcjonalnego zatrzymywania według p lub efektu; określić końcową datę i sposób raportowania niewystarczającej rekrutacji. Pilotaż nie wchodzi do próby głównej.

## Miary i analiza

Kanoniczne definicje: [manuskrypt](main.tex), [punktowanie](materials/README.md) i [plan analizy](materials/analysis-plan.md). H1: efekt przydziału w punktach procentowych skorygowany o pretest, warstwę i sekwencję. H2 analogicznie dla T2. H3 i H4 na skali naturalnej, z odpowiednią miarą bazową. Testy dwustronne, H1 alfa 0,05, Holm dla H2–H4. ANCOVA z HC3; wnioskowanie asymptotyczne wymaga weryfikacji. Raportować estymaty i 95% CI, liczebności i braki. Przy brakach 50 imputacji PMM i reguły Rubina, jeśli zatwierdzona procedura jest wykonalna. Analiza kompletnych przypadków i przesunięcia MNAR -5/-10 pp w każdym ramieniu jako wrażliwość; model pozycji GLMM jako analiza dodatkowa. Próg minimum 20/24 odpowiedzi lub par pewność–odpowiedź, 5/6 ocen uzasadnień. Nie zmieniać obserwowanych danych podczas imputacji. Jeżeli metoda nie zbiega się, raportować niepowodzenie i udokumentować odstępstwo; nie wybierać modelu na podstawie istotności.

## Zmiany, dane i etyka

Zachować osobno plan przed zamrożeniem, zamrożoną rewizję, zmiany datowane po zamrożeniu i analizy eksploracyjne. Przygotować informację dla uczestnika, podstawę i zakres przetwarzania, retencję, oddzielenie kontaktów od pseudonimów, procedurę wycofania i dostęp do danych. Nie publikować surowych danych ani finalnych kluczy przed akwizycją. Udostępnienie zanonimizowanych danych podlega odrębnej decyzji. Prerejestracja OSF lub inny rejestr dopiero po ustaleniu wersji, autoryzacji właściciela i weryfikacji aktualnej dostępności rejestracji.

## Niezamknięte decyzje przed rejestracją

1. Eksperci, pilotaż poznawczy i ilościowy, równoważność form, finalny bank pod kontrolą dostępu.
2. Minimalny efekt istotny edukacyjnie, N, daty i rekrutacja; warstwowanie i alokacja.
3. Walidacja symulacyjna pełnego mechanizmu braków sesji, kalibracja wnioskowania i niezależna kontrola GLMM.
4. Zatwierdzenie etyczne, dokumenty uczestnika i zasady danych.
5. Manifest zamrożonych wersji, testy exact SHA i autoryzacja rejestracji.

Nie oznaczać jako prerejestrowane, dopóki nie ma rzeczywistego potwierdzenia rejestru.
