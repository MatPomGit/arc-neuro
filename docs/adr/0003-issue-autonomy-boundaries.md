# ADR-0003: Issues jako plan, nie autoryzacja wykonania

**Data:** 2026-11-20  
**Status:** proposed

## Kontekst

Prace ARC Neuro wymagają powiązania z Research Autopilot i wymaganą zgodą właściciela, ale samo Issue nie może stawać się nową kolejką wykonawczą lub nadawać uprawnień do publikacji.

## Decyzja proponowana

GitHub Issues rejestrują pojedyncze wyniki, kryteria odbioru, zależności i kanoniczny blok `agent-work-classification:v1`. Formularze ułatwiają intake. Natywne Parent/Blocked by używamy tylko po faktycznej weryfikacji API. Etykieta `ready-for-agent` ani znacznik klasyfikacji nie uruchamia zadania; kontroler Research Autopilot pozostaje jedynym schedulerem. Zgody naukowe, publikacyjne i infrastrukturalne są niezależnymi bramkami.

## Alternatywy i skutki

Automatyczny bot po zmianie etykiety byłby prostszy, ale miesza sugestie, autoryzację i wykonanie. Kontrakt fail-closed wymaga uzupełnienia metadanych oraz potwierdzenia źródeł, lecz chroni przed przypadkowym uruchomieniem.
