# Protokół E01 i gotowość pomiaru

MSC-EYE-P01 · 1.0.0 · Mateusz Pomianek. Źródło aparatury i kontraktu pomiarowego to [ARC Mobile Eye Tracking na 6f0e3fd](https://github.com/MatPomGit/arc-mobile-eyetracking/tree/6f0e3fd92447448532bb2617f96b07d347d043b1). Repozytorium źródłowe przechowuje kontrakt, plan E00–E04 i rejestr dowodów. Aktualny zestaw dowodów nie obejmuje pomiarów uczestników ani porównania z referencją laboratoryjną.

## Projekt E01

Propozycja do pilotażu: dwie wizyty w odstępie 2–7 dni, powtórzenie tego samego warunku bazowego na tym samym urządzeniu, świeża kalibracja na każdej wizycie. Przypiąć konfigurację: model telefonu, orientację portretową, wersję Androida, model estymatora i konfigurację kalibracji. Przed każdą wizytą sprawdzić geometrię, faktyczne wymiary aktywnej części ekranu i odległość oka. Zapisać układ współrzędnych oraz sposób oszacowania rzutu oka. Warunki zmienne wprowadzić w osobnych blokach po podstawowym E01.

Proponowana kalibracja zawiera dziewięć punktów w siatce 3 × 3. Finalny zestaw oceny zawiera dwanaście punktów, w tym obwodowe oraz pośrednie, bez pokrywania współrzędnych kalibracyjnych. Cele ustalić na podstawie wersjonowanej siatki zawierającej fizyczne współrzędne i identyfikatory. Ocenę przeprowadzić w dwóch blokach po dwanaście prób z niezależnymi permutacjami. Pilotaż sprawdza parametry 1,5 s ekspozycji i okno od 0,5 do 1,3 s, liczone od czasu pojawienia się celu. Dokumentować straty ramek i rozbieżność pomiędzy zegarem bodźca i próbek. Pierwszy blok stanowi ocenę główną, drugi służy do analizy wewnątrzsesyjnej.

Próba wymaga ważnej inicjalizacji i co najmniej 10 prawidłowych próbek w oknie. Regułę minimalnego pokrycia czasowego potwierdzić w pilotażu i zamrozić wraz z limitem ewentualnych powtórzeń. Powtórzenie po awarii oznaczyć jako dodatkowe i uwzględnić analizę pierwszej próby. Raportować planowane próby, udane próby, liczbę osób bez wyniku, błędy na celach i dyspersję w oknie (mediana odległości od mediany punktu).

## Projekt analizy i przejście

Pilotaż ustali empiryczną wariancję median osoby i oczekiwaną utratę pomiaru. Przed ustaleniem N określić docelową szerokość 95% przedziału dla średniej median oraz oddzielnie dla dostępności. Symulować całe osoby, z korelacją prób i wzorcem braków zależnym od warunku. Analiza główna korzysta z bootstrapu osób, a w E02 kontrasty zmian wewnątrzosobniczych używają resamplingu par. Oprócz mediany raportować 90. i 95. percentyl oraz lokalizację błędów na ekranie.

Bramki przed udziałem ludzi: wersjonowana implementacja, kwalifikacja E00 na pełnym torze, zatwierdzona procedura E01 i właściwa decyzja etyczna. Eksport ma zawierać współrzędne pochodne, znacznik monotoniczny, identyfikatory protokołu i wersji oraz przyczyny braków. Surowego wideo i obrazów twarzy nie utrwala się domyślnie. Wyników indywidualnych nie zapisuje się w publicznym repozytorium.
