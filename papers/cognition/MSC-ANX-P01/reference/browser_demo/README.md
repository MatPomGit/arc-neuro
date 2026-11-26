# Lokalny demonstrator MSC-ANX-P01

## Lokalny demonstrator przeglądarkowy (P3.6a)

Wygeneruj manifest w Pythonie, uruchom statyczny serwer wyłącznie na loopback i otwórz adres localhost. Wczytaj plik JSON ręcznie. Prototyp bez formularzy zdrowotnych, identyfikatorów uczestników, sieciowej akwizycji, pamięci trwałej, telemetrii i publikacji Pages. Eksport DEMO jest jawnie niezgodny z wejściem analiz syntetycznych. Nie udostępniać uczestnikom badania.

```sh
cd papers/cognition/MSC-ANX-P01/reference
python3 export_demo.py /tmp/anx-demo.json --seed 42
python3 -m http.server 8765 --bind 127.0.0.1 --directory browser_demo
# Otwórz http://127.0.0.1:8765/ w przeglądarce i wybierz /tmp/anx-demo.json.
# Testy kontraktu JS, Node >=20:
ANX_DEMO_MANIFEST=/tmp/anx-demo.json node --test browser_demo/core.test.mjs
```

Implementacja: 336 prób, mapowanie F/J, wskazówka 300 ms, deadline klasyfikacji 2000 ms, ITI 500 ms, przerwy między blokami, kontrola fokusu, odrzucanie powtórzonych zdarzeń klawiszy, rozróżnienie timeout i błędu technicznego. RT = timestamp zdarzenia klawiatury minus znacznik aktualizacji DOM w requestAnimationFrame; nie jest to potwierdzony fizyczny onset. Próg 150 ms nadmiarowego czasu wskazówki jest wstępny. Trening i sprawdzanie zrozumienia dodano w P3.6b; nadal brak końcowej walidacji timing na różnych przeglądarkach i gwarancji rzeczywistej ekspozycji. Przed pilotażem potrzebne: testy E2E w przeglądarce, kontrola urządzenia i opóźnień, zatwierdzone skale, instrukcje i zgoda etyczna. Nie zastępuje przyszłej aplikacji kanonicznej.

## Trening, kontrola rozumienia i E2E (P3.6b)

Manifest demonstratora v0.3.0: dwa osobne bloki treningu po 24 próby, z odrębnych ziaren zachowujących mapowanie klawiszy. Trening przed pierwszą próbą klasyfikacji (także gdy decyzje są pierwsze), wymagane 18 poprawnych odpowiedzi w przedziale 150–2000 ms; jedno powtórzenie. Błędy techniczne i timeout nie zaliczają próby treningowej. Brak zaliczenia drugiej próby pomija wyłącznie klasyfikację; niezależne zadanie pozostaje dostępne. Przed pierwszym zadaniem decyzyjnym trzy pytania sprawdzające rozumienie prawdopodobieństw; po błędzie instrukcja i jedno ponowne podejście; po drugim niepowodzeniu pomija się obie domeny wyboru. Raport DEMO oddziela trening od 336 prób właściwych i zawiera diagnostykę czasu wskazówka–aktualizacja DOM, a nie fizyczny onset. Progi pozostają projektowe. Nie zbiera się danych uczestników.

Test E2E Chromium: `ANX_CHROME=/usr/bin/google-chrome python3 browser_demo/e2e.py` (w izolowanym venv z playwright==1.56.0). CI używa przeglądarki Chrome z obrazu publicznego runnera, bez publikacji. Kontrolowane zdarzenie blur testuje reakcję kodu, nie rzeczywiste opóźnienie przełączenia okna. Kolejność domen risk/ambiguity jest równoważona przez dodatkowy bit ziarna. Deadline zachowuje 2000 ms według timestamp zdarzenia, z 50 ms buforem obsługi kolejki; niespójny zegar i nadmierny lag oznaczają błąd techniczny. Przed badaniem pozostaje walidacja wieloprzeglądarkowa i sprzętowa, audyt dostępności, instrukcje, zgoda etyczna i kanoniczne środowisko.
