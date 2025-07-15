
import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="article_db",
        user="article_user",
        password="Div@2003!"
    )
