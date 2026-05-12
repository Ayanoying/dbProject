import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="h303database",
        user="appuser",
        password="appuser123",
        host="localhost",
        port=5432
    )