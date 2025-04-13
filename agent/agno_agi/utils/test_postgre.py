import psycopg
from dotenv import load_dotenv
import os
load_dotenv()
postgres_user = os.getenv("POSTGRES_USER")
postgres_password = os.getenv("POSTGRES_PASSWORD")
print(postgres_user,postgres_password)
conn = psycopg.connect(f"dbname=ai user={postgres_user} password={postgres_password} host=localhost port=5432")
print("Kết nối thành công!")
conn.close()
