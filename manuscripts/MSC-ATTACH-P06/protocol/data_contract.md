# Kontrakt eksportu CA przed implementacją formularza

Status: kontrakt eksportu 0.1.0. Walidator i pierwszy etap analizy są dostępne w [software/pilot_ca](../analysis/README.md). Formularz i jego integracja nadal wymagają wdrożenia oraz sprawdzenia G07/G08. Model logiczny rozdziela harmonogram, próby odpowiedzi i wartości; eksport nie może zawierać tylko kompletnych formularzy, bo utraciłby informację o brakach.

## Prywatne tabele

| Plik | Klucz | Minimalne pola |
|---|---|---|
| participants.csv | participant_code | instrument_version, schedule_started, start_offset, withdrawal_offset (nullable), completion_status |
| prompts.csv | participant_code + day + prompt | planned_offset_s, enabled_before_withdrawal, delivery_status, delivered_offset_s (nullable) |
| submissions.csv | submission_id | participant_code, day, prompt, opened_offset_s, submitted_offset_s (nullable), closed_offset_s (nullable), end_reason, instrument_version, help_open_count |
| items.csv | submission_id + item_id | displayed, value (nullable), response_status, displayed_offset_s (nullable), answered_offset_s (nullable) |
| changes.csv | change_id | relative_time, affected_record_id, field, old_value, new_value, reason, operator_code, processing_version |

W ESM dzień ma zakres 1–7, prompt 1–6. Czasy to sekundy od wspólnego początku harmonogramu danej osoby, nie czas od otwarcia każdego formularza. W prywatnym źródle technicznym zachować strefę czasową/zmiany zegara; analizy używają monotonicznego czasu trwania, jeśli telefon go udostępnia. Kod osoby jest losowy, nie inicjałami. Nie zapisywać danych identyfikujących partnera.

`delivery_status`: `confirmed`, `failed`, `unknown`. `end_reason`: `submitted`, `abandoned`, `technical_error`. `response_status`: `answered`, `skipped`, `structural`, `not_reached`, `technical_error`. Nie kodować braku jako 0, -999 ani wartości 50.

Dla każdej rozpoczętej próby zapisać dziesięć rekordów pozycji: na pierwszym prompcie dnia cztery pozycje przedziałowe mają `displayed=false`, `response_status=structural`, wartość i czasy puste. Niewyświetlona pozycja po przerwaniu ma `not_reached`, nie `skipped`. Pozostałe niewyświetlone rekordy nie wchodzą do mianownika braków wśród wyświetlonych. Wartość `answered` musi należeć do zakresu ze słownika; `K_contact` przyjmuje tylko 0 lub 1. Zmiana skali albo identyfikatora wymaga nowej wersji instrumentu.

## Zasady wyprowadzania wyników

1. Zachować wszystkie zaplanowane prompty, także bez żadnego formularza; po rezygnacji anulować wysyłki, lecz pozostawić plan z oznaczeniem anulowania. Nie generować odpowiedzi.
2. Wysłanie jest terminowe, gdy submitted_offset_s mieści się w zamkniętym przedziale od planned_offset_s do planned_offset_s + 1200 i harmonogram jest aktywny. Samo rozpoczęcie przed terminem nie wystarcza.
3. Dla pomiaru wybrać pierwsze terminowe wysłanie. Pozostałe próby zachować jako duplikaty. Bez terminowego wysłania formularz nie jest zrealizowany, a wartości późne/przerwane nie wchodzą do podstawowych rozkładów CA-M2/CA-D1.
4. Czas i brak odpowiedzi CA-F2/CA-M1 raportować dla wszystkich rozpoczętych prób oraz oddzielnie dla wybranych wysłań. Duplikaty nie mogą zwiększać liczby zrealizowanych promptów. Brak wartości w wybranym wysłaniu nie unieważnia całego wysłania.
5. Wystąpienie technicznego błędu pomiaru nie jest dowodem niskiej autonomii ani braku motywacji. Wykluczenie rekordu technicznego ma jawny kod i trafia do przepływu danych.
6. Korelacje opisowe dotyczą współwystępujących odpowiedzi przy tym samym prompcie. X_distance jest retrospekcją przedziału, a A_state oceną bieżącą; taki związek nie ustanawia kolejności przyczynowej. Nie nazywać go testem przewidywania następnego działania.

## Przechowywanie i wtórne użycie

Surowy eksport jest niezmienny; poprawki tworzą pochodne pliki i rejestr changes. Pliki mają sumy SHA-256, datę eksportu, wersję formularza i skryptu. Prywatne katalogi: raw / derived / logs / consent / linkage / exports. Dane kontaktowe i zgody są odseparowane od kodów analitycznych, dostęp jest przypisany rolom. Miejsce, termin retencji i warunki wycofania muszą zostać rzeczywiście ustalone w G03, nie są domyślnie „zatwierdzone”.

Domyślnie publiczne są kod, puste szablony, dane syntetyczne i zanonimizowane zestawienia. Zgoda na udział nie jest automatyczną zgodą na dowolne przyszłe badania lub publiczne udostępnienie. Zakres wtórnego wykorzystania należy ustalić przed rekrutacją. Nie gromadzić dodatkowych danych tylko dlatego, że mogą się kiedyś przydać.

`.gitignore` chroni umowny katalog `private_data/` przed przypadkowym dodaniem; nie jest kontrolą dostępu ani gwarancją bezpieczeństwa. Wypełnione rejestry także trzymać poza repozytorium. Przed udostępnieniem agregatów sprawdzić małe grupy i kombinacje mogące identyfikować osoby.

## Uściślenia wykonawcze kontraktu 0.1.0

Nagłówki czterech tabel wejściowych są dokładnie określone w `SCHEMAS` modułu `../analysis/analysis.py`; kolejność kolumn ma znaczenie. CSV: UTF-8 (opcjonalny BOM), puste pole oznacza brak, flagi `true`/`false`, wartości liczbowe z kropką i bez jednostki w komórce. `completion_status`: `completed`, `withdrawn`, `ongoing`, `not_started`; `help_open_count` jest nieujemną liczbą całkowitą.

`closed_offset_s` rejestruje koniec obserwowanej próby, także przerwanej. Przy wysłaniu równa się `submitted_offset_s`; przy przerwaniu może być nieznany i wtedy czas próby pozostaje brakujący. Nie wyliczać czasu przerwania z arbitralnego czasu ostatniej odpowiedzi. To uzupełnienie formatu przed danymi, nie zmiana pytania lub progu naukowego.

Każda rozpoczęta osoba ma wszystkie 42 wiersze harmonogramu, również po rezygnacji. `schedule_started=false` oznacza brak wierszy harmonogramu i status `not_started`. Przy rezygnacji zachowuje się czas i status `withdrawn`. Prompt jest aktywny, gdy jego czas planowany nie przekracza czasu rezygnacji; wysłania po rezygnacji nie są wybierane nawet wtedy, gdy formularz otwarto wcześniej.

`confirmed` wymaga czasu dostarczenia; `failed` i `unknown` mają ten czas pusty. Brak potwierdzenia transportu nie wyklucza sam w sobie ważnego formularza: realizację harmonogramu i realizację wśród potwierdzonych dostarczeń raportuje się oddzielnie. Remis czasów dwóch terminowych wysłań jest błędem niejednoznaczności do wyjaśnienia, nie powodem wyboru korzystniejszej odpowiedzi.

Walidacja kluczy i spójności czasów nie dowodzi poprawnego losowania powiadomień, aktywnego czasu na ekranie ani zgodności z ustawieniami telefonu. To osobne testy integracji G07.


Proweniencja: Mateusz Pomianek, ARC Attachment Dynamics, 9ddb0708dfcd380bcdc5a33f3a52d3b3c8df4b62, CC-BY-4.0. Zmieniono odwołania do katalogu analizy.
