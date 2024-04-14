# PYVO - PYthon VOting system
Univerzální hlasovací systém

![pyvo](https://github.com/Studenti-pro-studenty/pyvo/assets/44552607/b28c5cf5-64c8-4c74-9060-ea8de9676656)

## Adresář presets
Obsahuje přednastavené profily, podle kterých se vytváří tabulky v databázi.

## Soubor pyvo.db
Soubor SQLite databáze, pro načtení jiného presetu je potřeba ho přesunout nebo odstranit.

## Instalace závislostí
```commandline
cd pyvo/src
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Spuštění
```commandline
cd pyvo/src
python main.py
```
