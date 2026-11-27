# M02: ocena uwag metodologicznych, 2026-10-08

Uwagi wskazują trafne kierunki rozwoju. Wdrożenie nowych analiz nie zmienia wcześniejszych wyników w analizę potwierdzającą i nie gwarantuje cytowalności pracy. Poniżej rozdzielono wykonane zmiany od propozycji wymagających innego modelu wnioskowania.

| Uwaga | Ocena i realizacja |
|---|---|
| Niezależne trajektorie | Wdrożono i wykonano 8 960 triad, 26 880 trajektorii: osobne innowacje dla dopasowania, wyboru i testu. Zakres: te same zyski i schemat wymuszenia, z własną przyczynową historią każdej trajektorii. To nie gwarantuje poprawnej selekcji ani generalizacji na ludzi. |
| Purged Group TimeSeriesSplit | Nie jest konieczny dla niezależnie generowanych trajektorii. Skończona przerwa nie resetuje automatycznie pamięci regulatora i sprzężenia; alternatywa wymaga analizy zaniku zależności. |
| AIC/BIC | Wdrożono porównanie z walidacyjnym RMSE. Liczba parametrów obejmuje współczynniki, wyraz wolny i wariancję. To kryteria roboczej gaussowskiej wiarygodności, szczególnie ograniczone przy clippingu, błędach predyktorów i kategoriach. |
| BMS | Odroczono. Wymaga jawnych priorów parametrów/modeli oraz właściwej wiarygodności obserwacji. BIC nie jest tutaj obliczonym czynnikiem Bayesa. |
| FIM i profile | Wdrożono warunkową informację regresji PID oraz profile przy ustalonych predyktorach i znanej roboczej wariancji. Wyraźnie odróżniono je od niewdrożonej wiarygodności pełnego układu, propagującej zmiany parametrów przez stan i pomiar. Nie dowodzą identyfikowalności strukturalnej. |
| Tolerancja ε | Zachowano pierwotne 0,005; wykonano jawną analizę wrażliwości dla 0,001/0,0025/0,005/0,01. Podano skalę względem SD innowacji akcji, bez interpretacji jako progu ważności klinicznej lub psychologicznej. |
| Bootstrap | Wdrożono percentylowy bootstrap średniej sparowanej różnicy, 2 000 losowań jednostek replikacyjnych. Nie resamplowano niezależnie punktów czasu ani strat dwóch modeli. Nie ogłoszono gwarantowanego pokrycia ani kontroli wielokrotności. |
| Permutacje | Nie zastępują automatycznie przedziału średniej. Wymagają adekwatnej hipotezy i wymienialności/symetrii. |
| Realizm pomiaru | Wykonano stress testy: t(3) o tej samej wariancji, nieregularne próbkowanie, siedmiokategorialna kwantyzacja. To projektowane transformacje syntetyczne, nie zwalidowany model pomiaru Likerta. |
| ARC i dyada | Rozwinięto dyskusję o ograniczeniu zakresu błędu, aliasingu reaktywności i ukrytych kanałach działania. Są to hipotezy projektowe; pojedyncza plant nie symuluje dwóch rzeczywistych osób ani nie mierzy tłumienia emocji. |
| Definicje | Wyodrębniono równość praw obserwacji, praktyczną ekwiwalencję średnich strat i odzyskanie rodziny z mianownikiem prób. |
| OSF | Przygotowano projekt dla przyszłej, odrębnej analizy. Nie złożono rejestracji i nie przedstawiono istniejących wyników jako prerejestrowanych. |

## Korekty interpretacji uwag

- Nieukaranie RMSE nie oznacza, że wyższy rząd zawsze poprawia walidację. Gwarancja monotoniczności dotyczy dopasowania modeli zagnieżdżonych do tej samej próby.
- W pełnej wcześniejszej siatce w kombinacji przeciwności dla PID wybrano nonlinear 13 razy, PI 10 i ARX 7, ale intercept tylko 2 i AR 0; 38/80 prób było niewykonalnych. Stwierdzenie o uniwersalnym faworyzowaniu prostych baseline'ów jest zbyt mocne. Historyczny test i obecna siatka wymagają odrębnych interpretacji.
- FIM warunkowa może pozostać pełnego rzędu pomimo szumu i słabego odzyskania rodziny. Błąd zmiennych i specyfikacja modelu są osobnym problemem od rzędu macierzy.
- Mała strata, nominalne rozpoznanie i precyzja parametrów pozostają osobnymi wynikami. Prerejestracja porządkuje ich testowanie, ale nie naprawia automatycznie źle dobranych założeń.

## Wyniki nowych analiz

Zobacz [wyniki źródłowe](results/m02_robustness_development/development_report.md), [projekt prerejestracji](OSF_PREREGISTRATION_DRAFT.md) i nowe sekcje manuskryptu. Nowe wyniki są rozwojowe; nie zastępują wcześniejszych archiwów.

## Zweryfikowane źródła

- Akaike (1974), DOI 10.1109/TAC.1974.1100705: [archiwum Institute of Statistical Mathematics](https://www.ism.ac.jp/akaikememorial/aic.html).
- Schwarz (1978), DOI 10.1214/aos/1176344136: [rekord wydawcy](https://projecteuclid.org/journals/annals-of-statistics/volume-6/issue-2/Estimating-the-Dimension-of-a-Model/10.1214/aos/1176344136.full) i metadata Crossref. Strony 461–464 potwierdzone w metadanych indeksów; rekord Crossref nie zwraca pola page.
- Raue i in. (2009), DOI 10.1093/bioinformatics/btp358: [tekst autorów](https://www.jeti.uni-freiburg.de/papers/Raue_Bioinformatics_printed_1923.pdf), [PubMed](https://pubmed.ncbi.nlm.nih.gov/19505944/).
- Bootstrap: [oficjalna dokumentacja SciPy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html). Implementacja M02 korzysta tylko z NumPy i percentyli; nie udaje BCa.
- Prerejestracja: [Center for Open Science](https://www.cos.io/initiatives/prereg).
