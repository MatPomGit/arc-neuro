# ARC H1 ESM: polska wersja kandydacka

Wersja: **0.2-pl-cognitive**  
Status: kandydat do pilotażu poznawczego i pilotażu wykonalności. Nie jest jeszcze zamrożonym narzędziem badania potwierdzającego.

## Założenia

Minimalny prompt mierzy tylko zmienne wymagane przez H1 oraz prespecyfikowany kontekst. Stały rdzeń zawiera osiem pozycji, a maksymalnie dwie dalsze pozycje są warunkowe.

Dynamiczne znaczniki:
- `[partner]`: krótka etykieta wybrana przez uczestnika podczas onboardingu, np. imię, inicjał albo neutralne „partner/partnerka”;
- `[okres]`: dla pierwszego promptu dnia „od przebudzenia dzisiaj”, dla promptów 2-6 „od poprzedniego pomiaru”.

O ile nie wskazano inaczej, używana jest ciągła skala 0-100.

## A. Stan relacyjny teraz

### A1. Odczuwana bliskość, r_hat(t)

**Jaki poziom bliskości i więzi z [partner] odczuwasz w tej chwili?**

0 = brak bliskości i więzi  
100 = bardzo silna bliskość i więź

Zmienna: `r_hat_closeness`.

### A2. Pożądana bliskość, r*(t)

**Jakiego poziomu bliskości i więzi z [partner] chcesz w tej chwili?**

0 = brak bliskości i więzi  
100 = bardzo silna bliskość i więź

Zmienna: `r_star_closeness`.

A1 zawsze poprzedza A2. Obie pozycje używają identycznych kotwic. W pilotażu poznawczym trzeba sprawdzić, czy A2 jest rozumiane jako aktualnie pożądany stan, a nie globalny ideał związku.

### A3. Aktualny negatywny afekt

**Jak silne jest teraz Twoje napięcie, zdenerwowanie lub emocjonalny dyskomfort?**

0 = wcale  
100 = bardzo silne

Zmienna: `negative_affect`.

## B. Zdarzenia i kontakt w [okres]

### B1. Stresor relacyjny

**Czy [okres] wydarzyło się coś związanego z relacją z [partner], co wyraźnie zwiększyło Twoje napięcie lub dyskomfort?**

- nie
- tak

Zmienna: `relational_stressor`.

#### B1a. Siła wpływu stresora, tylko jeśli B1 = tak

**Jak silny był wpływ tego zdarzenia na Twoje samopoczucie w relacji?**

0 = znikomy  
100 = bardzo silny

Zmienna: `stressor_impact`.

### B2. Istotny kontakt

**Czy [okres] był kontakt z [partner] wykraczający poza krótką informację organizacyjną, np. rozmowa, wspólna aktywność lub wymiana emocji?**

- nie
- tak

Zmienna: `meaningful_interaction`.

Kontakt obejmuje formę bezpośrednią i zdalną.

## C. Regulacja w [okres]

### C1. Podejście / zwiększanie bliskości

**Na ile [okres] Twoje działania zmierzały do zwiększenia bliskości lub kontaktu z [partner], uzyskania wsparcia albo upewnienia się co do relacji?**

0 = wcale  
100 = bardzo silnie

Zmienna: `action_approach`.

### C2. Dystans / przestrzeń dla siebie

**Na ile [okres] Twoje działania zmierzały do zwiększenia dystansu lub przestrzeni dla siebie, ograniczenia kontaktu albo większej niezależności od [partner]?**

0 = wcale  
100 = bardzo silnie

Zmienna: `action_distance`.

C1 i C2 nie są wzajemnie wykluczające. W tym samym okresie obie wartości mogą być wysokie. C2 opisuje zachowanie dystansujące i nie jest bezpośrednim pomiarem autonomii ani unikania przywiązaniowego.

### C3. Wewnętrzne tłumienie / odsuwanie

**Na ile [okres] radzenie sobie z uczuciami związanymi z relacją polegało na ich tłumieniu, ignorowaniu lub odsuwaniu od siebie, bez bezpośredniego zmieniania kontaktu z [partner]?**

0 = wcale  
100 = bardzo silnie

Zmienna: `action_internal`.

C3 musi pozostać semantycznie odrębne od C2: C2 dotyczy zachowania wobec partnera lub kontaktu, a C3 sposobu obchodzenia się z własnymi uczuciami.

## D. Informacja zwrotna partnera

### D1. Perceived partner responsiveness, tylko jeśli B2 = tak

**Na ile podczas tego kontaktu było ze strony [partner] odczuwalne zrozumienie, akceptacja i gotowość do reagowania na Twoje potrzeby?**

0 = wcale  
100 = bardzo silnie

Zmienna: `partner_responsiveness`.

Pozycja ma status secondary/feedback i nie zastępuje zwalidowanej skali trait-level perceived partner responsiveness.

## Zmienne pochodne

`e_closeness = r_star_closeness - r_hat_closeness`

`action_signed = action_approach - action_distance`

`e_positive = max(e_closeness, 0)`

`e_negative = max(-e_closeness, 0)`

Surowe `action_approach` i `action_distance` są zawsze przechowywane, nawet jeśli główny model używa `action_signed`. `action_internal` pozostaje osobnym kanałem regulacji.

## Elementy celowo wyłączone z minimalnego promptu

Na tym etapie nie pytamy w każdym promptcie o:
- procent czasu spędzonego w kontakcie;
- fizyczną współobecność przez większość interwału;
- M, F, S ani dezorganizację;
- dodatkowe strategie regulacji;
- ogólną jakość relacji.

Elementy te mogą być badane w osobnych modułach, ale nie powinny zwiększać obciążenia pierwszego testu H1 bez osobnej hipotezy.

## Kryterium zamrożenia wersji

Wersja nie może zostać oznaczona jako `v1.0-confirmatory` przed:
1. dwiema rundami wywiadów poznawczych;
2. poprawnym rozróżnianiem A1 i A2;
3. poprawnym rozróżnianiem C2 i C3;
4. potwierdzeniem, że C1 i C2 mogą być jednocześnie wysokie;
5. pilotażem czasu wypełniania i działania powiadomień;
6. medianą czasu ukończenia promptu <= 90 s oraz kontrolą 90. percentyla;
7. zamrożeniem dokładnego brzmienia, kolejności, kotwic, logiki warunkowej i identyfikatorów zmiennych.

Szczegółowy protokół znajduje się w `cognitive_interview_plan.md`.
