# Przepływ metadanych, zatwierdzeń i publicznego katalogu

`msc-*/kanoniczny projekt` → ręczna kwalifikacja do ujawnienia → `portfolio/projects.json` i `portfolio/papers.json` → zapis decyzji w `portfolio/publication-approvals.json` (SHA-256, odnośnik do recenzji) → walidacja zewnętrznych powiązań i zgodności → `scripts/build_public_catalog.py` → **`pages/projects.md`** → odrębna decyzja o wdrożeniu strony.

Publiczne rejestry nie mogą zawierać nawet wyłączonych flagą prywatnych rekordów. `visibility: private` i `public_listing: false` nie są zabezpieczeniem przed ujawnieniem źródła w Git. W publicznym katalogu nie zapisujemy identyfikatorów sprzętu, danych EEG, okulometrii, wyników psychometrycznych ani nieanonimowych manifestów.

Generator dopuszcza wyłącznie publiczne, zatwierdzone projekty i ich kanoniczne adresy Pages. `docs/` służy do pracy nad metodami i politykami, `pages/` do świadomie przygotowanej prezentacji. Walidacja schematu lub skrótu nie zastępuje rzeczywistej decyzji właściciela i sprawdzenia zawartości publicznego HTML.

Test negatywny: wpis z prywatnym `repository` lub bez prawidłowego zatwierdzenia musi zostać pominięty. Puste rejestry powinny wygenerować pusty katalog bez fałszywych odwołań.
