import asyncio
import asyncpg
from dotenv import load_dotenv
import os
load_dotenv()
posgres_user = os.getenv("POSTGRES_USER")
posgres_password = os.getenv("POSTGRES_PASSWORD")
async def test_connection():
    try:
        conn = await asyncpg.connect(user=posgres_user, password=posgres_password,
                                     database='ai', host='localhost', port=5432)
        print("✅ Kết nối thành công!")
        # conn.execute("ALTER USER postgres WITH PASSWORD 'kty0928'")
        # print("✅ Đổi pass thành công!")
        await conn.close()
    except Exception as e:
        print("❌ Lỗi khi kết nối:", e)

asyncio.run(test_connection())