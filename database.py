import psycopg2
import os
from dotenv import load_dotenv


load_dotenv()

def get_connection():
    return psycopg2.connect(
        database=os.getenv("DB_NAME"), #your database name
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"), #your postgres sql password
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )   


#logic for create table and already exists
def table_ensure():
    try:
        connect=get_connection()
        cur=connect.cursor()

        cur.execute("""
            create table if not exists memorydata(
                id SERIAL,
                key text PRIMARY KEY ,
                value text
            )
        """)

        connect.commit()
        connect.close()
    except Exception as e:
        print("Ensure",e)

