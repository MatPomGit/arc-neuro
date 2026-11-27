# Strategia publikacyjna: MSC-CR-P11

**Data weryfikacji:** 2026-11-22. **Wersja:** 1.0.0. **Status:** robocza analiza dla projektu `IDEA_REVIEW`; nie przeprowadzono benchmarku ani nie zgłoszono manuskryptu.

**Tytuł:** Komputacyjny benchmark jakości argumentów i retoryki LLM.

## Ranking czasopism

| Priorytet | Czasopismo | ISSN | Punkty wykazu 2024 | Dopasowanie |
| --- | --- | --- | ---: | --- |
| Główny | Information Processing & Management | 0306-4573 | 140 | Rzetelność oceny informacji i argumentów, metody automatycznej ewaluacji, solidny benchmark |
| Ambitny, warunkowy | Expert Systems with Applications | 0957-4174 | 200 | Nowy algorytm lub framework oceny o istotnym wzroście jakości, generalizacji i odporności |
| Metodologiczny, warunkowy | Transactions of the Association for Computational Linguistics | eISSN 2307-387X | do potwierdzenia | Fundamentalny wkład w metody NLP, zasoby i ewaluację; wymagana szczególna nowość |

**Rekomendacja:** preferować *Information Processing & Management* (140 pkt). *Expert Systems with Applications* (200 pkt) jest celem ambitnym przy pełnej implementacji, wielomodelowych eksperymentach i silnych wynikach ilościowych. *Transactions of the Association for Computational Linguistics* jest opcją metodologiczną; punktacja wymaga niezależnego sprawdzenia przed wpisaniem wartości.

## Analiza nowości naukowej

W roku 2026 ukazał się **ArgBench: Benchmarking LLMs on Computational Argumentation Tasks**, integrujący 33 zbiory danych i 46 zadań argumentacyjnych. Opublikowano również badanie **Argument Quality Assessment with Large Language Models: A Pairwise Bradley-Terry Approach**, które obejmuje logiczny, retoryczny i dialektyczny wymiar argumentacji. Zatem sama kolejna ocena kilku modeli na standardowych zbiorach danych nie daje wystarczającej nowości.

Możliwe wyróżniki tego projektu to:
- **Ortogonalizacja jakości epistemicznej i siły retorycznej:** porównanie argumentów trafnych, lecz stylistycznie mało perswazyjnych, z argumentami wadliwymi, ale przekonującymi.
- **Walidacja niezależna od modelu:** nowe modele, nieznane domeny, parafrazy i warianty stylu nieobecne w danych uczących.
- **Odporność ocen:** testowanie, czy automatyczne wskaźniki mylą płynność wypowiedzi, deklarowaną pewność i spójność językową z jakością dowodu.
- **Zgodność ekspertów:** jawny kodeks oceny jakości dowodów, logiczności, uzasadnienia i retoryki, z raportowaniem niezgodności, nie jedynie zagregowanej średniej.

## Wymagania metodologiczne

1. Zdefiniować konstrukt „jakości argumentu” i odróżnić go od przekonującego tonu, płynności, emocjonalności i przyjmowalności przez odbiorcę.
2. Opracować niezależne zadania anotacyjne dla oceny poprawności przesłanek, trafności wnioskowania, zgodności dowodów z twierdzeniami oraz perswazyjności.
3. Ustalić klasy zadań i populację tekstów; dobierać kontrolowane kontrasty argumentów pod względem tonu i epistemicznej rzetelności.
4. Zabezpieczyć podziały treningowe/testowe przed przeciekiem tematów, źródeł i parafraz. Zastosować osobny test poza rozkładem (OOD).
5. Zaplanować anotację przez co najmniej dwóch niezależnych oceniających i procedurę rozstrzygania rozbieżności, z jawną oceną zgodności między sędziami.
6. Porównać proste baseline'y, klasyczne modele NLP, modele open-weight i metody LLM-as-a-judge. Rozważyć warianty bez dostępu do treści źródłowych i z dostępem do nich.
7. Raportować jakość klasyfikacji i rangowania odpowiednią do zadania (np. macro-F1, korelacje rang, błąd kalibracji), przedziały niepewności oraz analizę istotnych błędów.
8. Osobno raportować naruszenia odporności na parafrazy, zmiany domeny, kolejności argumentów i manipulacje perswazyjnością.
9. Przypiąć modele, prompty, zestawy danych, losowania i wersje kodu; sprawdzić licencje danych, prawa do publikacji anotacji i możliwość odtworzenia badań bez płatnych API.
10. Przed gromadzeniem danych lub anotacją z udziałem ludzi ustalić kwestie etyczne, wynagrodzenia anotatorów, przetwarzania danych i prawa do wykorzystania materiału.

## Ryzyka i interpretacja

Zgodność LLM-oceniającego z uśrednioną oceną ekspertów nie dowodzi rozumowania epistemicznego. Duża część istniejących zestawów benchmarkowych jest znana modelom, co podnosi ryzyko kontaminacji testów. Wysokie wyniki na parach parafraz mogą wynikać z podobieństwa leksykalnego, a nie z poprawnego rozpoznawania jakości argumentacji. Raportować oba składniki oddzielnie. Wyniki eksperymentów nie istnieją na tym etapie.

## Koszty i aktualność punktacji

Zakładany budżet obowiązkowych APC wynosi 0. Przed zgłoszeniem zweryfikować, czy wydawca oferuje tradycyjną ścieżkę bez obowiązkowego APC oraz dodatkowe opłaty i ewentualne umowy uczelniane. Punktacja 140/200 odpowiada wykazowi z 2024 r. i nie prognozuje punktacji w przyszłości. Nie przypisano kwartylów JCR ani kwot APC bez sprawdzenia dla konkretnego roku.

## Źródła

- [Information Processing & Management, punktacja 2024 – UJ](https://virt3.matinf.uj.edu.pl/czasopisma/229365-information_processing___management)
- [Expert Systems with Applications, punktacja 2024 – UJ](https://apacz.matinf.uj.edu.pl/czasopisma/228426-expert_systems_with_applications)
- [Information Processing & Management, profil wydawcy](https://shop.elsevier.com/journals/information-processing-and-management/0306-4573)
- [Expert Systems with Applications, profil wydawcy](https://shop.elsevier.com/journals/expert-systems-with-applications/0957-4174)
- [Transactions of the ACL, zakres i wymagania](https://transacl.org/ojs/index.php/tacl/about/submissions)
- [ArgBench: Benchmarking LLMs on Computational Argumentation Tasks, ACL 2026](https://aclanthology.org/2026.findings-acl.1099/)
- [Argument Quality Assessment with Large Language Models: A Pairwise Bradley-Terry Approach, EMNLP 2026](https://aclanthology.org/2026.findings-emnlp.1175/)
- [Prior Beliefs Prejudice LLM-as-Judge: Evidence from Persuasion Evaluation, ACL 2026](https://aclanthology.org/2026.findings-acl.2087/)

**Granice:** dokument nie stanowi zgłoszenia, akceptacji, wyników badań ani pozwolenia na publikację przez GitHub Pages.
