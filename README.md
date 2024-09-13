# Elections_scraper

Tretí projekt na Python Akadémiu od Engeta.

## Popis projektu

Tento projekt slúži k extrahovaniu výsledkov z parlamentých volieb ČR v roku 2017. Odkaz na výsledky nájdete [tu](https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ).

## Inštalácia knižníc

Knižnice, ktoré sú použité v kóde sú uložené v súbore `requirements.txt`. Pre inštaláciu odporúčam použiť nové virtuálne prostredie s nainštalovaným manažérom a spustiť nasledovne:

```python
$ pip3 --version                    # overim verziu manazera
$ pip3 install -r requirements.txt  # nainstalujem kniznice
```

## Spustenie projektu

Spustenie súboru `elections-scraper.py` v rámci príkazového riadku/terminálu požaduje dva povinné argumenty.

```python
python3 elections-scraper.py <odkaz-uzemneho-celku> <vysledny-subor>
```

Následne sa vám stiahnu výsledky ako súbor s príponou `.csv`.

## Ukážka projektu

Výsledky hlasovania pre okres Prostějov:

1. argument: `https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103`
2. argument: `vysledky_prostejov.csv`

Spustenie programu:

```
python3 elections-scraper.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" vysledky_prostejov.csv
```

Priebeh sťahovania:

```
STAHUJEM DATA Z VYBRANEHO URL: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103
UKLADAM DO SUBORU: vysledky_prostejov.csv
UKONCUJEM elections-scraper
```

Čiastočný výstup:

```csv
Code;Location;Registered;Envelopes;Valid;...
506761;Alojzov;205;145;144;29;0;0;9;0;5;17;4;1;1;0;0;18;0;5;32;0;0;6;0;0;1;1;15;0
589268;Bedihošť;834;527;524;51;0;0;28;1;13;123;2;2;14;1;0;34;0;6;140;0;0;26;0;0;0;0;82;1
...
```