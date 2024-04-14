# PYVO - PYthon VOting system
Univerzální hlasovací systém
| Hlasování | Výsledky |
| --------- | -------- |
|![pyvo](https://github.com/Studenti-pro-studenty/pyvo/assets/44552607/b28c5cf5-64c8-4c74-9060-ea8de9676656) | ![pyvo-results](https://github.com/Studenti-pro-studenty/pyvo/assets/44552607/7813fea9-7aa6-4576-bdd4-6bf5b84bcecd) |

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
