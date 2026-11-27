# Architektura programu ARC

`arc-*` pełni funkcję portalu naukowego i rejestru źródeł dowodów. `msc-*` jest właścicielem hipotez, protokołów, analiz, danych referencyjnych i manuskryptów, a `app-*` i `lib-*` dostarczają niezależne oprogramowanie. Duże istniejące projekty nie wymagają natychmiastowego przemianowania na `msc-*`.

```text
ARC (strategia, rejestry, publiczny katalog)
  |-- config/research-lines.json                dziedziny/linie naukowe
  |-- config/public-projects.json         kanoniczne badania i ich SHA
  |-- manuscripts/MSC-*/              własne manuskrypty
  |-- manuscripts/catalog.json       klasyfikacja i stan prac
  |-- site/projects.md                tylko publicznie zatwierdzone wpisy
  +-- [opcjonalne git submodules]     źródła projektów, nie kopie
          |-- msc-*                  nauka i strony badań
          +-- starsze repo           migracja kontrolowana
```

**Niezmiennik:** jedna pozycja artykułu -> jeden `owner_project_id` -> jedno kanoniczne repozytorium. Wieloprogramowe powiązania to tagi i `related`, nie duplikaty.

**Główne programy:** `arc-neuro`, `arc-ai`, `arc-xr`, `arc-robo`. Nie tworzyć `arc-ndd` ani `arc-eye`. Eye tracking jest rodziną metod i narzędzi.

**Dwa widoki SHA:** `snapshot_sha` służy do odtwarzania i wersjonowania indeksu; `remote_head_sha` jest odczytywany na żywo przez narzędzie audytu i nie zastępuje automatycznie snapshotu. Nie porównywać daty `README.md` z rzeczywistym stanem zdalnego repo.

**Sprzęt:** indeks zawiera wyłącznie zatwierdzone `equipment_id`, `contract_path` i `validation_status`. Pełne kontrakty aparatury pozostają przy badaniach kanonicznych. Nie utożsamiać standardowego Quest 3 z urządzeniem do śledzenia wzroku.


## Warstwy wykonawcze i decyzje

Własność programowa nie upoważnia do dostępu do danych badań ani wykonywania skryptów z repozytoriów podrzędnych. Publiczne metadane podlegają [przepływowi zatwierdzeń](docs/architecture/data-flow.md), a rozdział na `msc`, `app` i `lib` opisują [granice komponentów](docs/architecture/portfolio-boundaries.md).

Szczegóły techniczne: [reprodukowalność](docs/architecture/reproducibility.md), [model zagrożeń](docs/security/threat-model.md), [rejestr ADR](docs/adr/README.md). Niezależny standard [Issues](docs/issues.md) wspiera planowanie pracy, lecz nie tworzy nowego kontrolera.

**Rozdział prezentacji:** `docs/` to materiał roboczy, `site/` to jawnie wybrana publiczna projekcja. Generowany indeks zapisuje się wyłącznie w `site/projects.md`, nigdy przez automatyczny eksport `docs/`. Konfiguracja publikacji nadal wymaga zatwierdzenia właściciela.
