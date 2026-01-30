import psycopg

def get_connection():
    conn = psycopg.connect(
        host="localhost",
        dbname="Chatbot_History",
        user="postgres",
        password="78692",
        port=5432
    )
    return conn

conn=get_connection()