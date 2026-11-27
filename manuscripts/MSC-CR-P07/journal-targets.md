# Strategia publikacyjna: MSC-CR-P07

**Data opracowania:** 2026-11-22. **Wersja:** 1.0.0. **Status:** prospektywna selekcja czasopism; nie przeprowadzono badań ani nie zgłoszono artykułu.

**Tytuł:** Pewny ton pierwszej odpowiedzi LLM a bezkrytyczne przyjmowanie rekomendacji.

## Ranking czasopism

| Priorytet | Czasopismo | ISSN | eISSN | Punkty MNiSW, wykaz 2024 | Uzasadnienie |
| --- | --- | --- | --- | ---: | --- |
| Główny | Computers in Human Behavior | 0747-5632 | 1873-7692 | 140 | Psychologiczne mechanizmy polegania na AI, nadmierne zaufanie i przyjmowanie porad |
| Alternatywny | International Journal of Human-Computer Studies | 1071-5819 | 1095-9300 | 140 | Wpływ komunikowania pewności przez interfejs AI na wybory użytkownika |
| Rezerwowy | Current Psychology | 1046-1310 | 1936-4733 | 70 | Szerszy eksperyment psychologii osądu, wiarygodności i podatności na perswazję |

**Rekomendacja:** *Computers in Human Behavior* (140 pkt) jako pierwszy cel. *International Journal of Human-Computer Studies* (140 pkt) jest alternatywą przy wyraźniejszym wkładzie do projektowania komunikacji HCI. *Current Psychology* (70 pkt) to rezerwa dla ogólnopsychologicznej interpretacji.

Punktacja dotyczy wykazu z 5 stycznia 2024 r., nie przyszłej punktacji w roku publikacji.

## Ryzyko niewystarczającej nowości

W *Computers in Human Behavior* opublikowano już artykuły o nadmiernym poleganiu na poradach AI oraz wpływie pewności człowieka i AI na akceptację rekomendacji. Dlatego sama obserwacja, że „pewny ton zwiększa zaufanie”, byłaby niewystarczająca. Istotny wkład wymaga manipulacji pewnością językową przy **identycznej treści merytorycznej**, odrębnego pomiaru poprawności rekomendacji i kontroli wcześniejszej opinii uczestnika.

Przykładowe prace porównawcze:
- [Trust and reliance on AI — An experimental study on the extent and costs of overreliance on AI](https://doi.org/10.1016/j.chb.2024.108352) (*Computers in Human Behavior*, 2024).
- [Human confidence in artificial intelligence and in themselves: The evolution and impact of confidence on adoption of AI advice](https://www.sciencedirect.com/science/article/pii/S0747563221003411).
- [Is anthropomorphizing AI worth it? The role of hands-on experience in shaping advice uptake](https://www.sciencedirect.com/science/article/abs/pii/S0747563226000804) (*Computers in Human Behavior*, 2026).

## Sugerowany projekt eksperymentalny

1. Losowo manipulować językowym tonem pewności pierwszej odpowiedzi LLM (wysoki vs. ostrożny), nie zmieniając faktów, argumentów, długości ani struktury informacji poza niezbędną manipulacją stylistyczną.
2. Rozdzielić poprawność rekomendacji (poprawna vs. błędna) od tonu pewności. Wariant czynnikowy 2 × 2 jest szczególnie wartościowy: pozwala sprawdzić, czy ton zmienia selektywność polegania.
3. Zmierzyć ocenę uczestnika **przed poradą** oraz ostateczną decyzję **po poradzie**. Oddzielać akceptację poprawnych rekomendacji od błędnej akceptacji.
4. Pierwszorzędowy estymand: interakcja tonu pewności i poprawności porady na prawdopodobieństwo przyjęcia rekomendacji lub trafność ostatecznej decyzji. Wybrać dokładnie jedną pierwotną definicję przed prerejestracją.
5. Przewidzieć niezależny, zaślepiony klucz poprawności dla wszystkich zadań oraz ekspercką ocenę porównywalności treści. Wynikiem drugorzędowym może być kalibracja pewności osądu.
6. Model mieszany logistyczny z efektami uczestnika i zadania; z góry zdefiniować kontrasty, kontrolę wiedzy bazowej i poziomu doświadczenia z AI.
7. Wykonać pilotaż manipulacji: odbiorcy powinni odróżniać ton pewności, ale nie jakość faktograficzną odpowiedzi. Zamrozić bodźce i prompty; nie generować porad na żywo podczas głównego badania.
8. Zaplanować liczebność próby, procedurę zgody, kryteria jakości i retencję danych. Odróżnić efekt pierwszej odpowiedzi od efektów powtarzanej ekspozycji, nie przypisując mu skutków długoterminowych.

## Ryzyka interpretacyjne

- Akceptacja porady nie jest równoznaczna z błędem, jeśli porada jest poprawna.
- Zmiana tonu może zmieniać postrzeganą autorytatywność, uprzejmość i kategoryczność; efekty te warto rozdzielić w pilotażu.
- Efekt pierwszej odpowiedzi może być zakotwiczeniem lub efektem kolejności, nie specyficzną właściwością LLM.
- Uczestnicy mogą różnić się wiedzą domenową, doświadczeniem z AI i pewnością własnych odpowiedzi.
- Wyniki nie będą uzasadniały twierdzeń o trwałej utracie autonomii poznawczej ani przyczynach różnic indywidualnych poza manipulacją.

## Koszty i weryfikacja

Preferować publikowanie standardowe bez obowiązkowego APC tam, gdzie dopuszcza to model wydawcy. Przed wysłaniem manuskryptu ponownie sprawdzić aktualny wykaz punktowy, instrukcje autorów, opłaty dodatkowe i umowy transformacyjne. Brak zweryfikowanych kwot APC oraz kwartylów JCR, dlatego ich tutaj nie przypisano.

## Źródła bibliometryczne i strony czasopism

- [Computers in Human Behavior, 140 pkt w bazie APS](https://bw.aps.edu.pl/info/journalseries/WUT67670/)
- [International Journal of Human-Computer Studies, 140 pkt w bazie UJ](https://virt3.matinf.uj.edu.pl/czasopisma/229628-international_journal_of_human_computer_studies)
- [Current Psychology, wydawca](https://link.springer.com/journal/12144)
- [Computers in Human Behavior, wydawca](https://shop.elsevier.com/journals/computers-in-human-behavior/0747-5632)
- [International Journal of Human-Computer Studies, wydawca](https://shop.elsevier.com/journals/international-journal-of-human-computer-studies/1071-5819)

Dokument jest planem publikacyjnym. Badanie pozostaje w fazie `PROSPECTIVE`, a publikacja na GitHub Pages wymaga odrębnej zgody.
