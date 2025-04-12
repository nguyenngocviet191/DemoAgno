import psycopg
from dotenv import load_dotenv
import os
load_dotenv()
posgres_user = os.getenv("POSTGRES_USER")
posgres_password = os.getenv("POSTGRES_PASSWORD")

conn = psycopg.connect(f"dbname=ai user={posgres_user} password={posgres_password} host=localhost port=5432")
print("Kết nối thành công!")
conn.close()