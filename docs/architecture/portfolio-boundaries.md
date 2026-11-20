# Odpowiedzialność za komponenty i prace

| Warstwa | Źródło kanoniczne | Niedozwolone powielenie |
| --- | --- | --- |
| ARC Neuro | `program.json`, `areas/index.json`, zatwierdzone `portfolio/*.json` | Hipotezy, surowe dane i manuskrypty źródłowe |
| Projekt badawczy | Właściwy projekt `msc-*` lub uznane starsze repo | Drugi właściciel tego samego manuskryptu |
| Aplikacja | Repozytorium `app-*`, gdy faktycznie istnieje | Dublowanie kodu w każdym projekcie ARC |
| Biblioteka | Repozytorium `lib-*` tylko przy potwierdzonej potrzebie | Przedwczesne wyodrębnianie niewspółdzielonego kodu |
| Aparatura | Uzgodnione, uprawnione źródło kontraktów sprzętu | Prywatne identyfikatory i konfiguracje w publicznym katalogu |

`papers/` jest **neutralnym układem 63 slotów**, nie prawdziwą listą 63 publicznie zatwierdzonych manuskryptów. Potencjalnych tytułów, prywatnych mapowań i dowodów nie należy dopisywać do tych katalogów bez odrębnej zgody właściciela.

Relacja `related` wskazuje wspólne metody lub sprzęt, a nie powtórne przypisanie autorstwa. `snapshot_sha` służy odtworzeniu konkretnej rewizji; odczyt `remote_head_sha` służy sprawdzeniu aktualności źródła i nie aktualizuje historycznego snapshotu.
