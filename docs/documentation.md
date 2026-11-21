# Standard dokumentacji i limitów ARC Neuro

`config/documentation-policy.json` wyznacza limity **liczby znaków Unicode**, uwzględniając spacje i końce wierszy. Kontrola `scripts/validate_documentation.py` nie modyfikuje plików i jest uruchamiana w CI.

| Kategoria | Limit znaków |
| --- | ---: |
| `README.md`, `AGENTS.md`, `ARCHITECTURE.md` | 12 000 |
| `SECURITY.md`, workflow agentów | 10 000 |
| `GOVERNANCE.md`, `RESEARCH.md` | 9 000 |
| Pojedynczy ADR | 6 500 |
| Strona w `pages/` | 6 000 |
| `docs/issues.md` | 9 000 |

Nie wprowadza się limitów znaków dla pełnych manuskryptów, bibliografii, rzeczywistych protokołów i kodu. Pliki `papers/<obszar>/MSC-*/README.md` prezentują rzeczywiste tytuły i statusy szkiców naukowych. Nie stanowią rejestru zaakceptowanych publikacji ani źródła danych pomiarowych. Wydłużenie dokumentu z wynikami nie uzasadnia przeniesienia danych wrażliwych do ARC.

Zasada minimalnej redundancji: pojedynczy kontrakt i odnośniki z pozostałych dokumentów. Rejestry `portfolio/*.json`, stan `PROJECT_STATE.yaml`, zatwierdzenia oraz przegląd metod mają odrębne odpowiedzialności. Nie przenoś instrukcji technicznych z `docs/` do `pages/`.
