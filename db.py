import os
import psycopg2

conn = None

def init_db():
    global conn
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is not set!")
    conn = psycopg2.connect(database_url)
    return conn
