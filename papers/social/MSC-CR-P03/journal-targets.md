# Strategia publikacyjna: MSC-CR-P03

**Data przeglądu:** 2026-11-22. **Wersja:** 1.0.0. **Stan:** planowany manuskrypt, nie zgłoszono do redakcji.

**Temat:** Językowa dyfuzja norm w sieciach społecznych z AI.

## Ranking czasopism

| Priorytet | Czasopismo | ISSN | Punkty w wykazie 2024 | Dopasowanie |
| --- | --- | --- | ---: | --- |
| Główny | Computers in Human Behavior | 0747-5632 | 140 | Psychologiczne mechanizmy wpływu komunikatów AI na normy i zachowanie społeczne |
| Ambitny, warunkowy | New Media & Society | 1461-4448 | 200 | Społeczne mechanizmy platform, komunikacja i dyfuzja norm; wymagana istotna nowość teoretyczna i silna walidacja |
| Alternatywny, warunkowy | Journal of Computer-Mediated Communication | 1083-6101 | 200 | Procesy komunikacji zapośredniczonej oraz wymiana treści między ludźmi i AI; wymaga mocnego wkładu komunikologicznego |

**Decyzja:** preferować *Computers in Human Behavior* (140 pkt). Dwa czasopisma za 200 pkt są celami ambitnymi i wymagają innego poziomu walidacji oraz wyraźniejszego wkładu w teorię mediów i komunikacji, nie jedynie symulacji.

## Specyfika planowanego badania

Aktualny `main.tex` zakłada symulację rozpowszechniania norm na sieciach z komunikatami ludzkimi i AI przy kontrolowanej topologii. Proponowany główny estymand to różnica prawdopodobieństwa przyjęcia normy pomiędzy warunkami z komunikatami AI i ludzkimi, przy tej samej strukturze sieci i początkowym rozkładzie norm.

Należy jasno rozróżnić:
- **adopcję normatywną**: akceptację lub deklarowane poparcie dla normy;
- **dyfuzję komunikatu**: dalsze przekazywanie treści;
- **polaryzację**: wzrost odległości między rozkładami przekonań lub powstawanie klastrów;
- **agenta symulacyjnego** od ludzkiego uczestnika, ponieważ zachowania symulowanych agentów nie są dowodem zachowań społecznych ludzi.

## Warunki zwiększenia szans publikacyjnych

1. Ustalić co najmniej trzy kontrolowane warunki: tekst ludzki, tekst wygenerowany przez LLM i tekst neutralny; rozważyć również manipulację ujawnieniem autorstwa.
2. Zamrozić topologie sieci (np. losowe, małego świata, zróżnicowane stopniem), rozmiary sieci, warunki początkowe i procedury losowania.
3. Oddzielnie mierzyć przyjęcie normy i przekazanie komunikatu; wybrać jedno pierwotne kryterium sukcesu.
4. Weryfikować zgodność znaczeniową i stylistyczną komunikatów oraz przeprowadzić zaślepioną ocenę konstruktu.
5. Raportować rozkład efektów między topologiami, wariantami modeli, nasionami losowymi i parametrami symulacji; ocenić wrażliwość i niepewność.
6. Zapewnić walidację zewnętrzną, najlepiej eksperyment behawioralny z rzeczywistymi uczestnikami lub wiarygodne dane zastane z właściwymi zgodami. Bez niej ograniczyć wnioski do modelu symulacyjnego.
7. Przerejestrować protokół i kontrolować liczbę hipotez, rodzinę testów oraz procedurę raportowania wyników zerowych.

## Ograniczenia i koszty

Symulacja z udziałem LLM nie daje podstaw do stwierdzeń o populacyjnej skali rzeczywistej dyfuzji norm. Silne efekty modelowe mogą zależeć od promptu i topologii. Nie wolno używać realnych danych społeczności bez sprawdzenia uprawnień, zasad platform i kwestii etycznych.

Preferowana ścieżka publikacji zakłada brak obowiązkowego APC. Model publikowania, opłaty dodatkowe, aktualne limity objętości oraz możliwości umów instytucjonalnych wymagają ponownego sprawdzenia przed zgłoszeniem. **Punkty są stanem wykazu 2024, a nie prognozą przyszłej punktacji.**

## Źródła

- [Ministerstwo Nauki: wykaz 5.01.2024](https://www.gov.pl/web/nauka/komunikat-ministra-nauki-z-dnia-05-stycznia-2024-r-w-sprawie-wykazu-czasopism-naukowych-i-recenzowanych-materialow-z-konferencji-miedzynarodowych)
- [UJ: Computers in Human Behavior, 140 pkt](https://apacz.matinf.uj.edu.pl/czasopisma/227380-computers_in_human_behavior)
- [UJ: New Media & Society, 200 pkt](https://virt3.matinf.uj.edu.pl/czasopisma/232743-new_media___society)
- [UJ: Journal of Computer-Mediated Communication, 200 pkt](https://virt3.matinf.uj.edu.pl/czasopisma/230419-journal_of_computer_mediated_communication)
- [Computers in Human Behavior, opis zakresu](https://shop.elsevier.com/journals/computers-in-human-behavior/0747-5632)
- [New Media & Society, instrukcja dla autorów](https://journals.sagepub.com/author-instructions/nms)

Nie przeprowadzono symulacji, walidacji na ludziach ani recenzji wydawniczej. Ten dokument nie zatwierdza publikacji na GitHub Pages.
