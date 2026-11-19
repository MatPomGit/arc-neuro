# Polityka CI i publikacji ARC Neuro

Publiczne kontrole struktury i testy jednostkowe uruchamia workflow `arc-contract-tests.yml` na izolowanym GitHub-hosted runner, osobno dla dokładnego SHA gałęzi PR i syntetycznego commitu scalającego. Sukces konfiguracji nie oznacza wykonania testów; decyzję podejmuje się na podstawie wyniku konkretnego SHA.

Konto uruchomieniowe ma tylko `permissions: contents: read`, a `actions/checkout` nie przechowuje poświadczeń. Nie stosować uprzywilejowanego `pull_request_target` do wykonywania niezaufanego kodu ani udostępniać sekretów, danych uczestników i źródeł niepublicznych.

Publikacja Pages, przeniesienie projektów, zmiany uprawnień i wydania wymagają osobnej zgody. Nie dopuszcza się dodatkowych opłat bez akceptacji właściciela.
