# Instrument kandydacki CA 0.1.0

Autorskie pozycje do sprawdzenia. Nie są walidowaną skalą ani tłumaczeniem skali z cytowanych publikacji. Źródłem identyfikatorów i typów danych jest `measurement_dictionary.csv`.

## Instrukcja dla uczestnika

Pytania dotyczą Twojej relacji z partnerem lub partnerką. Odpowiadaj o wskazanym momencie, a nie o związku w ogóle. Nie ma prawidłowych odpowiedzi. Możesz pominąć każde pytanie.

Przez dobrowolność rozumiemy poczucie, że postępujesz z własnego wyboru, w zgodzie ze sobą. Nie musi to oznaczać bycia osobno ani podejmowania wszystkich decyzji samodzielnie. Można z własnej woli wybierać bliski kontakt i wspólne decyzje.

Wybierz wartość od 0 do 100. Pola startują bez odpowiedzi; brak zaznaczenia nie oznacza 0 ani 50. Formularz pokazuje końce skali i wybraną wartość. Każde pytanie oceniasz niezależnie.

## Stan i cel teraz

| ID | Pytanie | 0 | 100 |
|---|---|---|---|
| C_state | Jak duża jest w tej chwili odczuwana przez Ciebie bliskość emocjonalna z partnerem lub partnerką? | brak bliskości emocjonalnej | bardzo duża bliskość emocjonalna |
| C_target | Jak duża miałaby być ta bliskość emocjonalna, żeby odpowiadała temu, czego chcesz w tej chwili? | brak bliskości emocjonalnej | bardzo duża bliskość emocjonalna |
| A_state | W jakim stopniu czujesz w tej chwili, że to, jak postępujesz w tej relacji, jest Twoim własnym, dobrowolnym wyborem? | zupełny brak poczucia dobrowolności | pełne poczucie dobrowolności |
| A_target | Jak duże poczucie dobrowolności w tym, jak postępujesz w tej relacji, odpowiadałoby temu, czego chcesz w tej chwili? | zupełny brak poczucia dobrowolności | pełne poczucie dobrowolności |

Kotwice stanu i celu w każdej parze są identyczne. A_target jest celowo trudnym kandydatem: niemal stałe maksimum może oznaczać nieprzydatność dynamicznego pomiaru celu w tym brzmieniu. Nie sugerować uczestnikom, że odpowiedź 100 jest błędem.

## Pytania rozróżniające, teraz

| ID | Pytanie | 0 | 100 |
|---|---|---|---|
| P_pressure | Jak silnie czujesz teraz, że musisz postępować w tej relacji w sposób, którego sama lub sam nie wybierasz? | wcale | bardzo silnie |
| W_solitude | Jak silnie chcesz teraz spędzić trochę czasu osobno od partnera lub partnerki? | wcale | bardzo silnie |

Presja jest osobnym kandydatem; nie kodować jej automatycznie jako `100 - A_state`.

## Działania od poprzedniego powiadomienia tego samego dnia

| ID | Pytanie | 0 | 100 |
|---|---|---|---|
| X_approach | W jakim stopniu próbowałaś lub próbowałeś zwiększyć bliskość emocjonalną lub kontakt z partnerem albo partnerką? | wcale | bardzo silnie |
| X_distance | W jakim stopniu próbowałaś lub próbowałeś zwiększyć dystans, uzyskać więcej przestrzeni lub ograniczyć kontakt z partnerem albo partnerką? | wcale | bardzo silnie |
| X_internal | W jakim stopniu próbowałaś lub próbowałeś odsunąć od siebie uczucia dotyczące relacji bez bezpośredniej zmiany kontaktu z partnerem albo partnerką? | wcale | bardzo silnie |

**K_contact:** Czy w tym okresie był między Wami kontakt, który był dla Ciebie znaczący (także telefoniczny lub przez wiadomości)? Odpowiedzi: nie / tak / pomijam.

Na pierwszym powiadomieniu każdego dnia cztery pozycje przedziałowe nie są wyświetlane i mają brak strukturalny. Kolejne pytania odnoszą się do poprzedniego *zaplanowanego* powiadomienia tego dnia, również gdy odpowiedź na nie pominięto. Formularz wyświetla godzinę początku przedziału. Brak kontaktu nie zeruje automatycznie żadnego kanału działania.

## Wywiad kognitywny: instrukcja dla badacza

1. Poproś o samodzielne przeczytanie instrukcji i odpowiedź. Nie wyjaśniaj znaczenia przed pierwszą próbą.
2. Dla każdej z czterech głównych pozycji zapytaj: „Co to pytanie znaczy własnymi słowami?”, „O jakim czasie myślisz?”, „Co odróżnia tę ocenę od drugiego pytania w parze?”.
3. Dla A_state/A_target zapytaj: „Czy wspólna decyzja może być dobrowolna?”, „Czy bycie samemu zawsze oznacza dobrowolność?”.
4. Przedstaw cztery winiety poniżej, naprzemiennie w kolejności 1–4 lub 4–1 między kolejnymi osobami. Poproś o niezależną ocenę bliskości i dobrowolności oraz uzasadnienie. Zapisz kolejność.
5. Sprawdź P_pressure versus A_state, W_solitude versus X_distance oraz X_distance versus X_internal. Zapytaj, czy obie akcje X_approach i X_distance mogły wystąpić w jednym okresie.
6. Dopiero po zakodowaniu pierwszej odpowiedzi możesz wyjaśnić pojęcie. Zachowaj osobno wynik przed i po wyjaśnieniu; wynik po wyjaśnieniu nie zalicza kryterium zrozumiałości.
7. Na koniec zapytaj o brakujące sytuacje, trudne słowa, dyskomfort i czas odpowiedzi. Nie proś o dane identyfikujące partnera.

### Winiety i klucz dla badacza

1. Osoba czuje więź i z własnej woli wybiera wspólny wieczór: wysoka bliskość, wysoka dobrowolność.
2. Osoba czuje więź, lecz uczestniczy w spotkaniu pod presją, wbrew sobie: wysoka bliskość, niska dobrowolność.
3. Osoba nie czuje teraz więzi i z własnej woli zajmuje się własnym projektem: niska bliskość, wysoka dobrowolność.
4. Osoba nie czuje więzi i wbrew sobie dostosowuje zachowanie do nacisku partnera: niska bliskość, niska dobrowolność.

Winiety wprost opisują zamierzone współrzędne. Sprawdzają rozumienie instrukcji, nie trafność ocen rzeczywistych osób. Nie wymagaj konkretnej liczby na skali. W rejestrze używaj kodów `state_target`, `timeframe`, `autonomy_distance`, `autonomy_control_partner`, `anchors`, `interval`, `other`, `none`. Dla każdego pytania i każdej winiety zapisz `pass`, `fail` lub `unclear` z krótkim, zanonimizowanym uzasadnieniem.
