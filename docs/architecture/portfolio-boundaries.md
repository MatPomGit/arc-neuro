# Odpowiedzialność za komponenty i prace

| Warstwa | Źródło kanoniczne | Niedozwolone powielenie |
| --- | --- | --- |
| ARC Neuro | `program.json`, `areas/index.json`, zatwierdzone `portfolio/*.json` | Hipotezy, surowe dane i manuskrypty źródłowe |
| Projekt badawczy | Właściwy projekt `msc-*` lub uznane starsze repo | Drugi właściciel tego samego manuskryptu |
| Aplikacja | Repozytorium `app-*`, gdy faktycznie istnieje | Dublowanie kodu w każdym projekcie ARC |
| Biblioteka | Repozytorium `lib-*` tylko przy potwierdzonej potrzebie | Przedwczesne wyodrębnianie niewspółdzielonego kodu |
| Aparatura | Uzgodnione, uprawnione źródło kontraktów sprzętu | Prywatne identyfikatory i konfiguracje w publicznym katalogu |

`papers/` zawiera obecnie **69 nazwanych szkiców i koncepcji** (63 historyczne wpisy, trzy późniejsze `MSC-ZAH-*` oraz trzy prospektywne projekty `MSC-ANX-P01`, `MSC-FAT-P01` i `MSC-INTERO-P01`). Ten publicznie widoczny katalog roboczy **nie** ustanawia kanonicznej własności manuskryptów, ich statusu empirycznego ani zgody na publikację przez GitHub Pages. Zamrożony historyczny zbiór 63 identyfikatorów opisuje `config/historical-manuscripts-63.txt`; zatwierdzona projekcja `pages/` pozostaje odrębna. Przed rejestracją, przeniesieniem lub nadaniem statusu kanonicznego nowym pracom trzeba potwierdzić ich właściciela naukowego i repozytorium źródłowe w osobnej decyzji. Nie wolno ujawniać prywatnych mapowań ani danych badawczych.

Relacja `related` wskazuje wspólne metody lub sprzęt, a nie powtórne przypisanie autorstwa. `snapshot_sha` służy odtworzeniu konkretnej rewizji; odczyt `remote_head_sha` służy sprawdzeniu aktualności źródła i nie aktualizuje historycznego snapshotu.
