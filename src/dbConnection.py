import psycopg2
import os

def get_connection():
    return psycopg2.connect(
        dbname="h303database",
        user=os.getenv("USER", "iman"),
        password="",
        host="localhost",
        port=5432
    )