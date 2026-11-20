# Model zagrożeń ARC Neuro

**Status: model do weryfikacji, nie raport potwierdzonego zabezpieczenia.**

| Granica | Zagrożenie | Kontrola i jej dowód |
| --- | --- | --- |
| `portfolio/*.json` | Ujawnienie prywatnej pracy nawet przy `public_listing=false` | Jedynie jawnie dopuszczone rekordy, testy negatywne i przegląd praw do ujawnienia |
| Zatwierdzenia | Spreparowany SHA lub fikcyjna recenzja | `verify_public_reviews.py`, realna recenzja właściciela i ochrona gałęzi |
| Repo i Issues | Prywatne mapowanie 63 slotów, dane uczestników lub identyfikatory aparatury | Zakaz przechowywania w publicznym Git, procedura incydentów |
| GitHub Pages | Publikacja `docs/` z promptami i notatkami roboczymi | Izolowany `pages/`, allowlista, skan i ręczna ocena wynikowego HTML |
| PR i CI | Wykonanie niezaufanego kodu z sekretami na trwałym runnerze | Hostowany, izolowany CI bez sekretów i bez uprawnień zapisu |
| Autopilot | Label lub `agent-work-classification:v1` mylony z autoryzacją | Kontroler poza ARC, weryfikowane uprawnienia, brak auto-dispatch |
| Metadane naukowe | Przypisywanie nieistniejącego DOI, publikacji lub wyników | Weryfikacja źródła, jawny status i brak automatycznej promocji |

Dla krytycznych przypadków należy potwierdzić na finalnym SHA wynik negatywny i zakres uprawnień. Nie deklaruj `PASS` dla konfiguracji ruleset, jeśli nie została zweryfikowana w rzeczywistym GitHub. Bieżąca blokada ochrony `main` znajduje się w [Issue #7](https://github.com/MatPomGit/arc-neuro/issues/7). Zobacz [SECURITY.md](../../SECURITY.md) i [incydenty](incident-response.md).
