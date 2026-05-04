# dbProject

Ce projet INFOH303 consiste à créer une base de données pour une plateforme de gestion de cours. Les données sont insérées dans une base PostgreSQL.

## Prérequis
- Python 3.10 ou plus
- PostgreSQL installé 
- Installer les modules nécessaires : pandas, psycopg2

## Structure du projet
- `src/parsers/` : fichiers de parsing
- `src/repositories/` : fichiers d'intégration des données parsées
- `src/services/` : gestion de l'application en terminal
- `res/data/` : fichiers données (CSV, JSON, XML)
- `res/schema/` : fichiers des tables SQL

## Créez un environnement virtuel, puis installez les dépendances (WSL Ubuntu):
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install psycopg2
pip install pandas
```

## Utilisation
1. Utiliser les identifiants PostgreSQL dans `dbConnection.py`
2. Créer la base de données : psql -U postgres -d h303database -f res/schema/schema.sql
3. Lancer le script : python3 src/main.py
4. Vous pouvez réinitialisé la database avec ./reset_db.sh

## Fait par :

- Kallouch Iman
- Descamps Joseph
- Josephy Cedric
- De Meester De Ravestein David

