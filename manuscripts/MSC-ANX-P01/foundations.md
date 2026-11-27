# MSC-ANX-P01: podstawy naukowe (v0.4.0, 2026-11-26)

**Scientific owner i autor szkicu:** Mateusz Pomianek (MatPomGit). **Status:** IDEA_REVIEW, PROSPECTIVE. Publiczny prospekt, nie zatwierdzony protokół ani drugi kanoniczny manuskrypt.

## Wkład i granice
Wspólna próba umożliwia ocenę relacji GAD-7 z kosztem zmiany reguły oraz dwoma odrębnymi kontrastami wyborów. Badanie obserwacyjne; nie identyfikuje mechanizmu neuronalnego, mediacji przyczynowej ani diagnozy. H1 jest główna; H2–H3 drugorzędowe (Holm); H4 eksploracyjna. Nie deklarujemy nowości światowej bez szerszego przeglądu.

## Mapa dowodów
| Obszar | Źródło i znaczenie |
|---|---|
| Kontrola uwagi | [Shi i in. 2019](https://pubmed.ncbi.nlm.nih.gov/31306935/): metaanaliza, uzasadnia odrębne RT i trafność. |
| Kliniczny GAD | [Metaanaliza 2025](https://pubmed.ncbi.nlm.nih.gov/40513710/): trafność może ulegać zmianie; populacja kliniczna nie jest odpowiednikiem GAD-7. |
| Wyniki niejednoznaczne | [Wong i Yu 2026](https://doi.org/10.3758/s13415-025-01349-2): brak istotnych skorygowanych związków z kosztami w afektywnym paradygmacie. |
| Decyzje | [Hartley i Phelps 2012](https://doi.org/10.1016/j.biopsych.2011.12.027), [Levy i in. 2010](https://pubmed.ncbi.nlm.nih.gov/20032238/): rozdzielenie ryzyka i niejednoznaczności. |
| Psychometria | [Hedge i in. 2018](https://doi.org/10.3758/s13428-017-0935-1): rzetelność różnic indywidualnych; [polska walidacja GAD-7 i PHQ-9 (2025)](https://doi.org/10.1007/s12144-025-07646-w). |
| Pomiar online | [Bridges i in. 2020](https://doi.org/10.7717/peerj.9414): sprawdzić timing konkretnej implementacji. |

Przegląd ukierunkowany, nie systematyczny. Następny etap: PubMed, PsycINFO, Scopus (jeśli dostęp), bez ograniczenia daty dla prac klasycznych; zapisać datę, kwerendy, kryteria, deduplikację i powody wyłączeń. Kwerendy: (anxiety OR GAD) AND (task switching OR cognitive flexibility); (anxiety OR intolerance of uncertainty) AND (risk OR ambiguity) AND decision making; task switching AND reliability; GAD-7 AND Polish AND validation. Oddzielić badania kliniczne, stanowe, cechowe i wymiarowe oraz paradygmaty afektywne i neutralne.

## Kontrakt pomiarów (proponowany)
| Pole | Typ / zakres | Zastosowanie |
|---|---|---|
| participant_id | losowy pseudonim | łączenie zadań |
| protocol_version, stimulus_version, seed | wersje i liczba całkowita | reprodukcja |
| gad7_total | int 0–21, brak jeśli niepełny | H1–H4 |
| depression_total | int wg zatwierdzonej skali | model warunkowy |
| age_years, sleep_hours | lata, godziny poprzedniej nocy | współzmienne |
| os_family, browser_family, task_order | ograniczone kategorie | QA i współzmienne |
| decision_order | risk/ambiguity jako pierwsza domena | H2–H3 |
| task, block, trial_index | enum, int, int | identyfikacja prób |
| rule, cue, stimulus, mapping | kategorie | równoważenie |
| transition | switch/repeat/undefined | kontrast H1 |
| correct, focus_lost, timeout, technical_error | bool | QA/trafność |
| rt_ms | ms od prezentacji bodźca | H1, QA |
| option_side, target_chosen | str, bool | H2–H3 |
| outcomes, probabilities, ambiguity_bounds | struktury liczbowe | kontrasty wyborów |
| ev_difference, variance_difference | liczby tylko dla jawnych p | model H2 |
| nominal_payoff_contrast, ambiguity_width | liczby | model H3 |

Zachować rozróżnienie między brakami i zerami; nie zapisywać IP, nazwisk ani tekstów swobodnych. Zdarzenie pierwszej próby bloku ma transition=undefined; timeout to osobna flaga, nie poprawny RT. Dokładność liczona na próbach technicznie ważnych, timeout traktowany jako niepowodzenie odpowiedzi. Każdy identyfikator próby unikalny w obrębie uczestnika i zadania.

## Bramki
| Etap | Kryterium akceptacji |
|---|---|
| P1 | Sprawdzić metadane cytowań, pełny przegląd literatury, polskie skale i prawa do wersji. |
| P2 | Zatwierdzić etykę, administratora, retencję, instrukcje, procedurę PHQ-9 i plan ochrony danych; nie rekrutować wcześniej. |
| P3 | Zaimplementować zadania i testy losowania, zgodności reguł, identyfikowalności EV/wariancji, rejestracji RT i błędów; dane syntetyczne. |
| P4 | Pilotaż 30–50 osób, bez weryfikowania hipotez głównych; zrozumiałość, dropout, rzetelność, jakość timing, brak efektu sufitu/podłogi; z góry ustalić kryteria poprawy i powtórzenia. |
| P5 | Symulacja mocy w Pythonie, rzeczywiste stopnie swobody kategorii, precyzja H1–H3, plan braków, zamrożenie protokołu i prerejestracja. |
| P6 | Rekrutacja, zamknięcie próby według z góry ustalonej reguły, analiza dokładnej wersji, niezależny przegląd. |

Wstępne liczebności wynikają z przybliżenia Fishera, nie z obserwacji. Nie ma decyzji etycznej, danych ani kanonicznej implementacji akwizycji; dostępny jest lokalny demonstrator i referencyjny model syntetyczny. Nie zmieniać rejestru kanonicznego i Pages bez oddzielnej zgody.
