import os
import psycopg2
from pathlib import Path

# Permet de lire le .env et d'utiliser ses variables
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ[key] = value.strip("'\"")


def get_connection():

    dsn = os.getenv("DATABASE_URL")

    if dsn:
        sslmode = os.getenv("PGSSLMODE", "require")
        return psycopg2.connect(dsn, sslmode=sslmode)

    return psycopg2.connect(
        dbname=os.getenv("DB_NAME", "h303database"),
        user=os.getenv("DB_USER", "appuser"),
        password=os.getenv("DB_PASSWORD", "appuser123"),
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 5432)),
    )
