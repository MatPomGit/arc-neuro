# Zarządzanie programem ARC Neuro

**Źródło prawdy:** `program.json` (tożsamość programu), `PROJECT_STATE.yaml` (status), `areas/index.json` (pięć linii), `portfolio/projects.json` i `portfolio/papers.json` (wyłącznie zatwierdzone publiczne wpisy), `portfolio/publication-approvals.json` (bramka zgody). Nie twórz równoległego rejestru publikacji, którego nie da się zsynchronizować z tymi zasobami.

Program utrzymuje **indeks powiązań**. Właściciel projektu `msc-*` lub istniejącego repozytorium odpowiada za hipotezy, protokoły, analizę, manuskrypt i wyniki. `app-*` dostarcza aplikacje, `lib-*` biblioteki. ARC nie kopiuje cudzych danych ani wewnętrznych metadanych. Puste rejestry oznaczają brak zatwierdzonych publicznych wpisów, **nie brak prowadzonych badań**.

Katalog `papers/` zawiera 63 neutralne sloty organizacyjne w pięciu obszarach, po przyjęciu odrębnego PR. Nie identyfikują one autorów, tytułów, prywatnych repo ani liczby zaakceptowanych manuskryptów. Wpis do publicznego katalogu wymaga indywidualnej zgody, SHA-256 metadanych i rzeczywistej recenzji właściciela zgodnie z [polityką publikacji](docs/publication-policy.md). Dwa dodatkowe artefakty niewchodzące do puli prac nie są artykułami.

Każdy PR wymaga kontroli aktualnego HEAD i base SHA, proporcjonalnych testów, niezależnej recenzji i respektowania WIP. Szczegóły: [AGENTS.md](AGENTS.md), [procedura](.github/AGENT_WORKFLOW.md), [standard Issues](docs/issues.md). Agent nie może zatwierdzić własnych badań, zmienić uprawnień ani uruchomić publikacji. Scalenie kodu nie oznacza zezwolenia na udostępnienie danych, uruchomienie Pages lub zgłoszenie manuskryptu.

**Ryzyko R3** obejmuje ujawnienie informacji prywatnych, dane osób badanych, prawa autorskie, publikację i zmianę dostępu. Wymaga osobnej decyzji upoważnionego właściciela, niezależnie od wyniku CI. W razie braku dowodów zapisuj `UNAVAILABLE`, a nie `PASS`.
