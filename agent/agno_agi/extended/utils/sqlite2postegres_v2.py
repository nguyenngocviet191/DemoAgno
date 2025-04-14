from sqlalchemy import create_engine, MetaData, Table, Column, String, DateTime, text
from sqlalchemy.orm import sessionmaker
import sqlite3
import os
from dotenv import load_dotenv
import uuid 
load_dotenv()
postgres_user = os.getenv("POSTGRES_USER")
postgres_password = os.getenv("POSTGRES_PASSWORD")
print(postgres_user,postgres_password)
# Cấu hình kết nối
SQLITE_DB_PATH = "agno_agi/tmp/b5398dae-a482-4a23-a717-6616c2f84fe8.db"  # Đường dẫn đến file SQLite
POSTGRES_DB_URL = f"postgresql+psycopg://{postgres_user}:{postgres_password}@localhost:5432/ai"  # URL kết nối PostgreSQL

# Tên bảng
TABLE_NAME = "multi_agent_memory"
TABLE_NAME2 = "agent_memory"
# Hàm tạo bảng PostgreSQL với cột agent_id
def create_postgres_table(engine):
    metadata = MetaData()
    table = Table(
        TABLE_NAME,
        metadata,
        Column("id", String, primary_key=True),
        Column("agent_id", String),  # Thêm cột agent_id
        Column("memory_id", String),
        Column("user_id", String),
        Column("memory", String),
        Column("created_at", DateTime, server_default=text("CURRENT_TIMESTAMP")),
        Column("updated_at", DateTime, server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP")),
    )
    metadata.create_all(engine)
    return table

# Upload dữ liệu từ SQLite lên PostgreSQL
def upload_to_postgres(sqlite_files, postgres_url):
    # Kết nối PostgreSQL
    postgres_engine = create_engine(postgres_url)
    Session = sessionmaker(bind=postgres_engine)
    postgres_session = Session()

    # Tạo bảng PostgreSQL nếu chưa tồn tại
    create_postgres_table(postgres_engine)

    # Duyệt qua từng file SQLite
    for sqlite_file in sqlite_files:
        # Lấy agent_id từ tên file (giả sử tên file là agent_id.db)
        agent_id = os.path.splitext(os.path.basename(sqlite_file))[0]

        # Kết nối SQLite
        sqlite_conn = sqlite3.connect(sqlite_file)
        sqlite_cursor = sqlite_conn.cursor()

        # Đọc dữ liệu từ bảng agent_memory
        sqlite_cursor.execute("SELECT id, user_id, memory, created_at, updated_at FROM agent_memory")
        rows = sqlite_cursor.fetchall()

        # Kiểm tra và chỉ upload các bản ghi mới hoặc đã thay đổi
        for row in rows:
            memory_id, user_id, memory, created_at, updated_at = row

            # Kiểm tra xem bản ghi đã tồn tại trong PostgreSQL chưa
            existing_record = postgres_session.execute(
                text(f"SELECT updated_at FROM multi_agent_memory WHERE memory_id = :memory_id AND agent_id = :agent_id"),
                {"memory_id": memory_id, "agent_id": agent_id}
            ).fetchone()

            # Nếu bản ghi không tồn tại hoặc đã được cập nhật, thì upload
            if not existing_record or existing_record[0] < updated_at:
                insert_query = text(f"""
                INSERT INTO multi_agent_memory (id, agent_id, memory_id, user_id, memory, created_at, updated_at)
                VALUES (:id, :agent_id, :memory_id, :user_id, :memory, :created_at, :updated_at)
                ON CONFLICT (id) DO UPDATE SET
                    user_id = EXCLUDED.user_id,
                    memory = EXCLUDED.memory,
                    updated_at = EXCLUDED.updated_at;
                """)
                postgres_session.execute(insert_query, {
                    "id": str(uuid.uuid4()),  # Tạo id mới
                    "agent_id": agent_id,
                    "memory_id": memory_id,
                    "user_id": user_id,
                    "memory": memory,
                    "created_at": created_at,
                    "updated_at": updated_at,
                })

        # Đóng kết nối SQLite
        sqlite_conn.close()

    # Commit và đóng kết nối PostgreSQL
    postgres_session.commit()
    postgres_session.close()
    print("Upload completed.")
# Download dữ liệu từ PostgreSQL về SQLite
def download_to_sqlite(postgres_url, agent_id):
    # Kết nối PostgreSQL
    postgres_engine = create_engine(postgres_url)
    Session = sessionmaker(bind=postgres_engine)
    postgres_session = Session()
    sqlite_path = agent_id + ".db"  # Đường dẫn đến file SQLite mới
    # Nếu file SQLite chưa tồn tại, tạo file mới và kết nối
    sqlite_conn = sqlite3.connect(sqlite_path)
    sqlite_cursor = sqlite_conn.cursor()

    # Tạo bảng SQLite nếu chưa tồn tại
    sqlite_cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME2} (
        id TEXT PRIMARY KEY,
        user_id TEXT,
        memory TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Đọc dữ liệu từ PostgreSQL
    query = text(f"""
    SELECT memory_id AS id, user_id, memory, created_at, updated_at
    FROM {TABLE_NAME}
    WHERE agent_id = :agent_id
    """)
    result = postgres_session.execute(query, {"agent_id": agent_id})
    rows = result.fetchall()

    # Lọc các dòng memory_id mà file SQLite chưa có
    existing_ids = set(row[0] for row in sqlite_cursor.execute(f"SELECT id FROM {TABLE_NAME2}").fetchall())
    rows = [row for row in rows if row[0] not in existing_ids]

    # Insert dữ liệu vào SQLite
    for row in rows:
        sqlite_cursor.execute(f"""
        INSERT OR REPLACE INTO {TABLE_NAME2} (id, user_id, memory, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?)
        """, row)

    # Commit và đóng kết nối
    sqlite_conn.commit()
    sqlite_conn.close()
    postgres_session.close()
    print("Download completed.")

# Chạy chương trình
if __name__ == "__main__":
    # Upload dữ liệu từ SQLite lên PostgreSQL
    # sqlite_files = [SQLITE_DB_PATH]  # Danh sách các file SQLite cần upload
    # upload_to_postgres(sqlite_files, POSTGRES_DB_URL)
   
    # Download dữ liệu từ PostgreSQL về SQLite
    download_to_sqlite(POSTGRES_DB_URL, "b5398dae-a482-4a23-a717-6616c2f84fe8")