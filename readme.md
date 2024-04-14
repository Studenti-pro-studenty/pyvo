# PYVO - PYthon VOting system
Univerzální hlasovací systém

## Adresář presets
Obsahuje přednastavené profily, podle kterých se vytváří tabulky v databázi.

## Soubor pyvo.db
Soubor SQLite databáze, pro načtení jiného presetu je potřeba ho přesunout nebo odstranit.

## Instalace závislostí
```commandline
cd ~/pyvo/src
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Spuštění
```commandline
cd ~/pyvo/src
python main.py
```
