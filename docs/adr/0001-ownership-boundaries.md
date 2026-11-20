# ADR-0001: kanoniczna własność projektu

**Data:** 2026-11-20  
**Status:** proposed

## Kontekst

ARC Neuro ma pięć linii tematycznych, wiele planowanych artykułów i potencjalne powiązania z programami ARC-AI, ARC-XR i ARC-Robo. Duplikowanie manuskryptów, danych lub aplikacji utrudnia przypisanie właściciela i odtwarzalność.

## Decyzja proponowana

ARC jest właścicielem publicznego indeksu i relacji, a właściwe `msc-*` lub starsze projekty zachowują manuskrypt, metodologię i dowody. Kod aplikacji i bibliotek jest właścicielstwem odpowiednich rzeczywistych repozytoriów. Każdy publiczny artykuł ma jednego `owner_project_id`.

## Alternatywy i skutki

Monolit zmniejsza liczbę odnośników, lecz miesza odpowiedzialności; kopie w wielu ARC powodują konflikt statusów. Proponowane rozdzielenie wymaga walidacji metadanych i prowadzenia odnośników, ale nie wymaga tworzenia nowych repozytoriów bez potrzeby.
