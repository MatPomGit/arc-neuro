# Zasady zmian i przeglądu ARC Neuro

Czytaj po kolei: `program.json`, `PROJECT_STATE.yaml`, `RESEARCH.md`, `ARCHITECTURE.md`, `config/public-projects.json`, `docs/governance.md`.

1. To repozytorium przechowuje własne manuskrypty i indeksuje badania zewnętrzne; nie kopiuj cudzych manuskryptów, wyników pomiarów ani kodu `app-*` i `lib-*`.
2. Każdy manuskrypt ma jedno repozytorium kanoniczne i jedno `project_id`; odnośniki między programami są `related`, nie drugą kopią.
3. Przed audytem aktualnego programu wykonaj `python scripts/bootstrap.py --mode audit-live` z uwierzytelnionym dostępem do repozytoriów. Raportuj `CURRENT`, `STALE` i `UNAVAILABLE` osobno. Nie opieraj aktualnej recenzji wyłącznie na starym gitlinku.
4. Przed odtworzeniem wyników użyj przypiętego commitu i manifestu eksperymentu (`--mode reproduce`). Nigdy nie zastępuj zamrożonego SNAPSHOT aktualnym `main` podczas analizy historycznej.
5. Nie publikuj danych osobowych, surowych EEG/wideo/eye trackingu ani identyfikatorów niepublicznych projektów. Kontrakty aparatury utrzymywane są przez właścicieli badań; ARC prezentuje tylko zaakceptowane metadane.
6. Rozróżniaj `planned`, `source_written`, `tested`, `hardware_verified`, `submitted`, `published`; nie wymyślaj DOI, etyki, statystyk, potwierdzenia uploadu OSF ani dostępności urządzeń.
7. Dla każdego PR zachowuj exact SHA, przegląd techniczny i obowiązujące limity prac. Nie uruchamiaj niezaufanego kodu na uprzywilejowanej infrastrukturze ani nie wprowadzaj dodatkowych kosztów.
8. Publikacja GitHub Pages, migracja projektów i zmiany uprawnień wymagają oddzielnej zgody.
9. Repozytoria niepubliczne podlegają kontroli dostępu i nie są częścią publicznego katalogu; nie zakładaj, że masz do nich dostęp.
10. Nie kasuj ani nie archiwizuj historycznych repozytoriów bez mapy odwołań i potwierdzenia właściciela.

11. Mateusz Pomianek musi pozostać co najmniej jednym z autorów w `CITATION.cff` i metadanych repozytorium programu; dodatkowych współautorów wolno dodawać po potwierdzeniu wkładu. Nie nadpisuj automatycznie autorstwa niezależnych prac w `msc-*`.
12. Dla repozytoriów publicznych bezpieczne, izolowane kontrole CI **mogą** korzystać z GitHub-hosted runners. Sekrety, prywatny `audit-live` i kod niezaufanych PR muszą pozostawać poza uprzywilejowanymi środowiskami. Nie traktuj konfiguracji CI jako dowodu wykonania testów; wymagaj wyniku na dokładnym SHA.


## Granice publicznej witryny i Issues

Dla GitHub Pages używaj tylko `site/` z jawną listą `config/pages-policy.json`. `docs/`, `.github/`, `manuscripts/`, `equipment/` nie mogą stać się źródłem witryny. Nie publikuj instrukcji dla agentów, notatek edytorskich, opisów współtworzenia repo ani poufnych mapowań. Nie dodawaj `CONTRIBUTING.md`.

Przyjmowanie zadań i ich triage wykonuj zgodnie z [docs/issues.md](docs/issues.md). Nie twórz duplikatów Issues i PR, nie twórz alternatywnej kolejki. Jeden poprawny typ intencji z kanonicznego katalogu, pojedynczy `agent-work-classification:v1`, obowiązkowy wynik, zakres, testy i bramki. Natywne Parent/Depends on/Blocks potwierdzaj odczytem GitHub. Nie oznaczaj tekstowego linku jako relacji natywnej.

**DoR:** potwierdzone repo, base SHA, istniejące zależności, oczekiwany wynik, właściciel, ryzyko R0–R3, kontrola autoryzacji i plan testów. **DoD:** testy dokładnego SHA, przegląd techniczny, dokumentacja, weryfikacja rzeczywistego merge/deploy i pozostawione blokady. R2/R3 wymagają odpowiednich testów i kontroli ryzyka, nie wymagają niezależnego review; udostępnienie danych i publikacja wymagają dodatkowo decyzji właściciela. Etykiety, komentarze i klasyfikacja nie nadają prawa wykonania. Procedura: [.github/AGENT_WORKFLOW.md](.github/AGENT_WORKFLOW.md).


13. Publiczne katalogi roboczych artykułów w `manuscripts/` mają rzeczywiste nazwy `MSC-...`, tytuły i przypisania naukowe. Zakaz tworzenia anonimowych `slot-NNN` i ukrywania tytułów wyłącznie z powodu publiczności repozytorium. Ograniczenia jawności dotyczą poufnych danych, kodu i odnośników do prywatnych źródeł; zatwierdzenia Pages pozostają odrębne.

14. W każdej własnej publikacji i szkicu naukowym programu, także w `manuscripts/`, jawnie wskazuj `Mateusz Pomianek` jako właściciela naukowego (`scientific_owner`). W polach autora manuskryptu uwzględniaj go, gdy jest autorem pracy; nie usuwaj potwierdzonych współautorów i nie przypisuj autorstwa cudzych publikacji. Nie utożsamiaj właściciela naukowego z lokalizacją kanonicznych źródeł ani z podmiotem praw autorskich. Brak wpisu w publicznym portfolio nie unieważnia tego przypisania. Podczas tworzenia i audytu manuskryptów sprawdzaj zgodność deklaracji autora, README i metadanych bez fabrykowania niepotwierdzonych informacji.
