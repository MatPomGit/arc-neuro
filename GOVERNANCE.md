# Zarządzanie programem ARC Neuro

**Źródło prawdy:** `program.json` (tożsamość programu), `PROJECT_STATE.yaml` (status), `config/research-lines.json` (pięć linii), `config/public-projects.json` (publiczne metadane projektów zewnętrznych), `manuscripts/catalog.json` (katalog własnych szkiców), `config/publication-approvals.json` (bramka zgody). Nie twórz równoległego rejestru publikacji, którego nie da się zsynchronizować z tymi zasobami.

Program utrzymuje **indeks powiązań**. Właściciel projektu `msc-*` lub istniejącego repozytorium odpowiada za hipotezy, protokoły, analizę, manuskrypt i wyniki. `app-*` dostarcza aplikacje, `lib-*` biblioteki. ARC nie kopiuje cudzych danych ani wewnętrznych metadanych. Puste rejestry oznaczają brak zatwierdzonych publicznych wpisów, **nie brak prowadzonych badań**.

Katalog `manuscripts/` zawiera 69 nazwanych szkiców i koncepcji, z klasyfikacją w metadanych. Wpis projektu zewnętrznego do publicznego katalogu wymaga indywidualnej zgody, SHA-256 metadanych i rzeczywistej recenzji właściciela zgodnie z [polityką publikacji](docs/publication-policy.md). Dwa dodatkowe artefakty niewchodzące do puli prac nie są artykułami.

Każdy PR wymaga kontroli aktualnego HEAD i base SHA, proporcjonalnych testów, przeglądu technicznego i respektowania WIP. Szczegóły: [AGENTS.md](AGENTS.md), [procedura](.github/AGENT_WORKFLOW.md), [standard Issues](docs/issues.md). Niezależne review PR jest opcjonalne. Agent nie może zatwierdzić własnych badań, zmienić uprawnień ani uruchomić publikacji. Scalenie kodu nie oznacza zezwolenia na udostępnienie danych, uruchomienie Pages lub zgłoszenie manuskryptu.

**Ryzyko R3** obejmuje ujawnienie informacji prywatnych, dane osób badanych, prawa autorskie, publikację i zmianę dostępu. Wymaga osobnej decyzji upoważnionego właściciela, niezależnie od wyniku CI. W razie braku dowodów zapisuj `UNAVAILABLE`, a nie `PASS`.
