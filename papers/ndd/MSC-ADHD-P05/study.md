# MSC-ADHD-P05 — EEG Muse S Athena zsynchronizowane ze zdarzeniami regulacji

**Program:** `arc-neuro` · **obszar:** `ndd` · **rodzaj:** `MANUSCRIPT` · **etap źródłowy:** `ACTIVE`.

## Projekt badania

**Przedmiot:** EEG Muse S Athena zsynchronizowane ze zdarzeniami regulacji.

- **Proponowany wynik główny:** Nie określono dotychczas w rejestrze. Należy zdefiniować estymand, miarę i jednostkę analizy przed akwizycją.
- **Zakres i odrębność:** Wymaga odrębnego przeglądu nowości i porównania ze źródłowym protokołem.
- **Metodologia:** hipotezy, dobór próby lub scenariuszy, kryteria jakości, plan statystyczny i analiza wrażliwości wymagają potwierdzenia we właściwym projekcie. Ten plik nie potwierdza uzyskania wyników.
- **Powiązane MSC:** brak jawnego powiązania w rejestrze.

## Stanowisko badawcze

**`ST-01`**. Klasyfikacja `PROPOSED_BY_SCOPE`; kwalifikacja aparatury `NOT_VERIFIED`. Jest to propozycja organizacyjna, nie dowód gotowości stanowiska.

## Aplikacje

- **`app-regulation-mobile`** (`APP-ARC-02`): rola `PRIMARY`, decyzja `SOURCE_VALIDATION`; status repozytorium `PLANNED_NOT_CREATED`.
- **`app-eeg-neurolyze`** (`APP-ARC-03`): rola `SIGNAL_SOURCE`, decyzja `DEVICE_RIGHTS`; status repozytorium `ALTERNATE_EXISTING_APP`, istniejący odpowiednik `eeg-neurolyze`.

## Biblioteki

- **`lib-adapt`**: status `PLANNED_NOT_CREATED`, proponowana zależność przez `app-regulation-mobile`. Brak potwierdzonej integracji.
- **`lib-events`**: status `PLANNED_NOT_CREATED`, proponowana zależność przez `app-regulation-mobile`, `app-eeg-neurolyze`. Brak potwierdzonej integracji.
- **`lib-sig`**: status `RENAMED_PARTIAL_CORE`, proponowana zależność przez `app-eeg-neurolyze`. Brak potwierdzonej integracji.
- **`lib-sim`**: status `PLANNED_NOT_CREATED`, proponowana zależność przez `app-eeg-neurolyze`. Brak potwierdzonej integracji.

## Proweniencja i warunki realizacji

Szczegółowa proweniencja materiałów źródłowych, odwołania do repozytoriów niepublicznych i numery rewizji są przechowywane poza publiczną kartą.

Przed wykonaniem badania należy sprawdzić prawa do danych, kompletność protokołu, zgodę etyczną (jeżeli dotyczy), bezpieczeństwo aparatury oraz niezależność wyniku wobec innych manuskryptów. Wpisy biblioteczne i aplikacyjne są **planem**, nie deklaracją działającego API. Brak wyników oznacza `NOT_VERIFIED`, a nie wynik zerowy.


## Imported manuscript and scientific contracts

The complete source is [main.tex](main.tex). Prospective manuscript; not a completed study. The following contract snapshots complement the manuscript; their presence does not authorize participant recruitment.

- [contracts/docs/byod_cross_device_benchmark_protocol.md](contracts/docs/byod_cross_device_benchmark_protocol.md)
- [contracts/docs/data_management_plan.md](contracts/docs/data_management_plan.md)
- [contracts/docs/device_profile_specification.md](contracts/docs/device_profile_specification.md)
- [contracts/docs/ethics_safety_regulatory.md](contracts/docs/ethics_safety_regulatory.md)
- [contracts/docs/measurement_and_telemetry.md](contracts/docs/measurement_and_telemetry.md)
- [contracts/docs/sensorimotor_fusion.md](contracts/docs/sensorimotor_fusion.md)
- [contracts/docs/statistical_reporting_policy.md](contracts/docs/statistical_reporting_policy.md)
- [contracts/docs/telemetry_specification.md](contracts/docs/telemetry_specification.md)
