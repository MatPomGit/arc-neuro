# MSC-ADHD-S02 — Reprodukowany schemat zdarzeń recovery i deterministyczny replay

**Program:** `arc-neuro` · **obszar:** `measurement-methods` · **rodzaj:** `MANUSCRIPT` · **etap źródłowy:** `METHODS_DRAFT`.

## Projekt badania

**Przedmiot:** Reprodukowany schemat zdarzeń recovery i deterministyczny replay.

- **Proponowany wynik główny:** Nie określono dotychczas w rejestrze. Należy zdefiniować estymand, miarę i jednostkę analizy przed akwizycją.
- **Zakres i odrębność:** Wymaga odrębnego przeglądu nowości i porównania ze źródłowym protokołem.
- **Metodologia:** hipotezy, dobór próby lub scenariuszy, kryteria jakości, plan statystyczny i analiza wrażliwości wymagają potwierdzenia we właściwym projekcie. Ten plik nie potwierdza uzyskania wyników.
- **Powiązane MSC:** brak jawnego powiązania w rejestrze.

## Stanowisko badawcze

**`ST-00`**. Klasyfikacja `PROPOSED_BY_SCOPE`; kwalifikacja aparatury `NOT_VERIFIED`. Jest to propozycja organizacyjna, nie dowód gotowości stanowiska.

## Aplikacje

- **`app-regulation-mobile`** (`APP-ARC-02`): rola `PRIMARY`, decyzja `SOURCE_VALIDATION`; status repozytorium `PLANNED_NOT_CREATED`.

## Biblioteki

- **`lib-adapt`**: status `PLANNED_NOT_CREATED`, proponowana zależność przez `app-regulation-mobile`. Brak potwierdzonej integracji.
- **`lib-events`**: status `PLANNED_NOT_CREATED`, proponowana zależność przez `app-regulation-mobile`. Brak potwierdzonej integracji.

## Proweniencja i warunki realizacji

Szczegółowa proweniencja materiałów źródłowych, odwołania do repozytoriów niepublicznych i numery rewizji są przechowywane poza publiczną kartą.

Przed wykonaniem badania należy sprawdzić prawa do danych, kompletność protokołu, zgodę etyczną (jeżeli dotyczy), bezpieczeństwo aparatury oraz niezależność wyniku wobec innych manuskryptów. Wpisy biblioteczne i aplikacyjne są **planem**, nie deklaracją działającego API. Brak wyników oznacza `NOT_VERIFIED`, a nie wynik zerowy.


## Imported manuscript and scientific contracts

The complete source is [main.tex](main.tex). Methods manuscript; independent execution evidence remains pending. The following contract snapshots complement the manuscript; their presence does not authorize participant recruitment.

- [contracts/config/controller_rules.example.json](contracts/config/controller_rules.example.json)
- [contracts/config/core_session_state_machine.example.json](contracts/config/core_session_state_machine.example.json)
- [contracts/docs/challenge_event_operationalization.md](contracts/docs/challenge_event_operationalization.md)
- [contracts/docs/data_management_plan.md](contracts/docs/data_management_plan.md)
- [contracts/docs/recovery_feature_operationalization.md](contracts/docs/recovery_feature_operationalization.md)
- [contracts/docs/state_machine_specification.md](contracts/docs/state_machine_specification.md)
- [contracts/docs/telemetry_queue_contract.md](contracts/docs/telemetry_queue_contract.md)
- [contracts/docs/telemetry_specification.md](contracts/docs/telemetry_specification.md)
- [contracts/schemas/recovery_event.schema.json](contracts/schemas/recovery_event.schema.json)
- [contracts/schemas/telemetry_queue_record.schema.json](contracts/schemas/telemetry_queue_record.schema.json)
