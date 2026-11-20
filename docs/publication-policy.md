# Polityka publikacyjna programu

Każdy `msc-*` ma własną stronę GitHub Pages, jeśli materiały zostały zatwierdzone do otwartej publikacji. Program publikuje katalog, wybrane streszczenia i zweryfikowane DOI/URL. Preprinty trafiają do uprawnionych repozytoriów preprintowych; prerejestracje do właściwej usługi rejestracyjnej. Żaden DOI, status accepted/published ani wynik nie może zostać wpisany bez dowodu. Prawa czasopisma, licencje i etyka są weryfikowane indywidualnie.

**Bramka metadanych publicznych.** Przed dodaniem jakiegokolwiek rekordu do `portfolio/projects.json`, `portfolio/papers.json` lub `portfolio/dependencies.json` należy potwierdzić: jawny charakter repozytorium i adresów, uprawnienie do ujawnienia tytułów i autorów, zgodność DOI/statusu z dowodami oraz brak danych i identyfikatorów niepublicznych. `public_listing` jest żądaniem umieszczenia wpisu w katalogu, a nie dowodem zgody. Decyzję publikacyjną dokumentuje się w publicznym PR i zatwierdza przed scaleniem. Generacja katalogu nie zastępuje tego przeglądu.

## Zakres licencji programu

Plik [`LICENSE`](../LICENSE) zawiera standardową licencję MIT dla autorskiego kodu i dokumentacji ARC Neuro. Licencja nie obejmuje automatycznie tekstów manuskryptów, materiałów wydawców, zbiorów danych, wyników zewnętrznych projektów ani zasobów osób trzecich. Ich autorstwo, licencję i uprawnienia do publikacji należy ustalić oddzielnie przed dodaniem do katalogu.

## Bramka publicznego indeksowania

Sama deklaracja `public_listing=true` nie jest zgodą na publikację. Wymagany jest odrębny wpis w [rejestrze zatwierdzeń](../portfolio/publication-approvals.json), powiązany skrótem SHA-256 z całym rekordem projektu. Rejestr wymaga odnośnika do publicznej recenzji GitHub, której autor i treść muszą być **rzeczywiście sprawdzone przez osobę scalającą**. CI sprawdza jedynie składnię, kompletność i zgodność skrótu, nie weryfikuje autentyczności ani uprawnień recenzenta.

Domyślnie generator akceptuje wyłącznie witrynę GitHub Pages odpowiadającą wskazanemu publicznemu repozytorium (`https://OWNER.github.io/REPOSITORY/`). Niestandardowe domeny wymagają osobnego, zatwierdzonego rozszerzenia polityki. Do skutecznej bramki właścicielskiej zalecane jest wymuszenie recenzji w regułach ochrony gałęzi `main`. Bez sprawdzenia dowodu zgody nie wolno scalać PR z nowym wpisem w rejestrze. Rejestry pozostają puste do momentu odrębnej decyzji publikacyjnej.

W przypadku GitHub Pages akceptowany jest kanoniczny **adres główny** projektu, a nie dowolna podścieżka. Pliki JSON są parsowane restrykcyjnie: powielone klucze i niestandardowe wartości `NaN`/`Infinity` blokują generowanie katalogu zamiast powodować niejednoznaczną interpretację metadanych.

### Sprawdzenie publicznej recenzji

Przy każdym zatwierdzeniu projektu recenzja GitHub właściciela musi mieć treść dokładnie `APPROVE_PUBLIC_LISTING <project_id> sha256:<64_znaki_szestnastkowe>` (bez dodatkowych słów; identyfikator i skrót odpowiadają metadanym). Powinna wskazywać stan `COMMENTED` lub `APPROVED`, być dostępna publicznie i mieć datę zgodną z rejestrem. Pole `review_url` ma wskazywać samą recenzję PR, nie ogólny adres repozytorium.

Skrypt `scripts/verify_public_reviews.py` odpytuje publiczne API GitHub bez tokenów, weryfikuje identyfikator, adres, autora, treść, stan i datę recenzji. Jeśli recenzja nie istnieje albo API jest niedostępne, kontrola blokuje walidację. Gdy rejestr jest pusty, nie wykonuje żądań sieciowych. Nadal trzeba zweryfikować, czy projekt źródłowy jest rzeczywiście publiczny, czy właściciel ma prawo do ujawnienia treści i czy reguły gałęzi nie pozwalają omijać wymaganych kontroli.


**Źródła publicznej strony:** wyłącznie `pages/` z `config/pages-policy.json`; generator indeksu zapisuje `pages/projects.md`. `docs/`, `papers/` i `portfolio/` nie są bezpośrednimi źródłami stron. Publikację plików i metadanych autoryzuje się oddzielnie od zaakceptowania kodu. Szczegóły: [Pages](pages.md) i [ADR-0002](adr/0002-publication-boundaries.md).
