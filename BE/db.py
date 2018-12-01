from flask import current_app, g
import psycopg2

conn = None

def get_db_conn():
    global conn
    if conn is None:
        conn = psycopg2.connect(
            database=current_app.config['DB_NAME'],
            user=current_app.config['DB_USER'],
            host=current_app.config['DB_HOST'],
            password=current_app.config['DB_PASS']
        )
    return conn
