# Kanoniczne rejestry programu

- `projects.json`: lista niezależnych projektów, także istniejących pod dawnymi nazwami. Pola każdego wpisu: `id`, `title`, `repository`, `url`, `role` (`primary`/`related`), `primary_program`, `line`, `status`, `visibility`, `public_listing`, `default_branch`, `snapshot_sha`, `pages_url`, `submodule_path`.
- `papers.json`: `id`, `title`, `owner_project_id`, `canonical_repository`, `manuscript_path`, `stage`, `doi`, `preprint_url`, `preregistration_url`. Główny `owner_project_id` jest dokładnie jeden.
- `dependencies.json`: grupy `tools`, `equipment`, `datasets`. Rekord zawiera `project_id`, `ref` i — zależnie od kategorii — wersję/commit, `equipment_id`, `contract_path` albo manifest/checksum. Brak duplikacji kontraktów aparatury.
- `areas/index.json`: lista `lines` z `id`, `title`, `description`. W ARC Neuro należy rozważyć `ndd`, `affect`, `cognition`, `social`, `psychometrics`; nie robić z NDD piątego ARC.

**Publiczne źródło:** ten katalog należy do publicznego ARC Neuro. Żaden rejestr nie może zawierać metadanych prywatnych repozytoriów, także gdy `public_listing=false`. Generacja publicznego katalogu wymaga `public_listing=true`, `visibility=public` i poprawnego HTTPS, natomiast faktyczne dopuszczenie rekordu wymaga odrębnego zatwierdzenia zgodnie z [`docs/publication-policy.md`](../docs/publication-policy.md). Dotyczy to także rekordów artykułów, zależności i ścieżek.
