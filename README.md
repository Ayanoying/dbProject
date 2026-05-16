# dbProject

Ce projet INFOH303 consiste à créer une base de données pour une plateforme de partage de résumés de cours. Les données sont insérées dans une base PostgreSQL.

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

## Configuration PostgreSQL (à faire une seule fois)

1. Créer la base de données :
```bash
sudo -u postgres createdb h303database
```

2. Créer l’utilisateur PostgreSQL de l’application :
```bash
sudo -u postgres psql
```

Puis dans `psql` :
```sql
CREATE USER appuser WITH PASSWORD 'appuser123';
GRANT ALL PRIVILEGES ON DATABASE h303database TO appuser;
\q
```

3. Donner les droits sur le schéma public :
```bash
sudo -u postgres psql -d h303database
```

Puis dans `psql` :
```sql
GRANT USAGE, CREATE ON SCHEMA public TO appuser;
\q
```

## Initialisation de la base

4. Charger le schéma SQL :
```bash
psql -h localhost -U appuser -d h303database -f res/schema/schema.sql
```

## Lancement

5. Lancer l’application :
```bash
python3 src/main.py
```

6. Dans le menu principal, choisir :

- Charger les données initiales


## Réinitialisation

Pour repartir de zéro, vous pouvez utiliser :
```bash
psql -h localhost -U appuser -d h303database -f res/schema/schema.sql
```

Après une réinitialisation, il faut relancer l’application puis recharger les données initiales via le menu.

## Fait par :

- Kallouch Iman
- Descamps Joseph
- Josephy Cedric
- De Meester De Ravestein David

