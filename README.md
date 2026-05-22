# dbProject

Ce projet INFOH303 consiste à créer une base de données pour une plateforme de partage de résumés de cours. Les données sont insérées dans une base PostgreSQL.
Dans le cadre de ce projet, la sécurité n'est pas une priorité, il s'agit d'une démonstration fictive afin d'illustrer les concepts de base de données. Le client se connecte à la base de données via les paramètres configurés localement ou en ligne et une session utilisateur est créée lorsque l'utilisateur se connecte à l'application.

## Prérequis

- Python 3.10+
- PostgreSQL
- Linux ou WSL

## Structure du projet

- `src/parsers/` : fichiers de parsing
- `src/repositories/` : fichiers d'intégration des données parsées
- `src/services/` : gestion de l'application en terminal
- `src/views/` : gestion de l'interface graphique (PyQt6)
- `res/data/` : fichiers données (CSV, JSON, XML)
- `res/schema/` : fichiers des tables SQL
- `main.py` : point d'entrée de l'application
- `dbConnection.py` : gestion de la connexion à la base de données
- 

## Création d'un environnement virtuel et Installation des dépendances

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install psycopg2
pip install pandas
pip install PyQt6
```

> Note: commandes à taper à la racine du projet

## Configuration PostgreSQL (localement)

1. Créer la base de données

```bash
sudo -u postgres createdb h303database
```

2. Créer l’utilisateur PostgreSQL de l’application

```bash
sudo -u postgres psql
```

Puis dans `psql` :

```sql
CREATE USER appuser WITH PASSWORD 'appuser123';
GRANT ALL PRIVILEGES ON DATABASE h303database TO appuser;
\q
```

3. Donner les droits sur le schéma public

```bash
sudo -u postgres psql -d h303database
```

Puis dans `psql` :

```sql
GRANT USAGE, CREATE ON SCHEMA public TO appuser;
\q
```

## Configuration PostgreSQL (en ligne)

Pour faciliter l'accès à la base de données entre développeurs/administrateurs et depuis n'importe où, nous avons utilisé Neon, une plateforme de base données postgreSQL en ligne et **[OPEN SOURCE](https://github.com/neondatabase/neon)**, facile à configurer et installer.

1. Créer un compte sur [Neon](https://neon.tech/).
2. Créer un projet et une base de données.
3. Récupérer les informations de connexion (connection string) et placer le dans un fichier .env à la racine du projet, avec le format suivant :

```env
DATABASE_URL="CONNECTION_STRING"
```

## Création des tables et (ré)initialisation des données

### 1. Charger le schéma SQL (création des tables)

- Localement:

```bash
psql -h localhost -U appuser -d h303database -f res/schema/schema.sql
```

- En ligne:

```bash
psql 'CONNECTION_STRING' -f res/schema/schema.sql
```

> Note: remplacer `CONNECTION_STRING` par le connection string de votre base de données en ligne

### 2. Charger les données (initialisation des tables)

#### Avec script

```bash
python3 dbInit.py
```

#### Sans script

*Lancer l'application et choisir l'option chargement des données*

### 3. Réinitialiser la BDD (optionnel)

Refaire étape 1 et 2

## Lancement de l'application

```bash
python3 main.py
```

## Auteurs

- Kallouch Iman
- Descamps Joseph
- Josephy Cedric
- De Meester De Ravestein David
