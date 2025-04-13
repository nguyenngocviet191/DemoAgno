import sqlite3
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, JSON, DateTime
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from sqlalchemy import create_engine
import psycopg
import os
load_dotenv()
posgres_user = os.getenv("POSTGRES_USER")
posgres_password = os.getenv("POSTGRES_PASSWORD")

POSTGRES_DB_URL= f"postgresql+psycopg://{posgres_user}:{posgres_password}@localhost:5432/ai"
# Đường dẫn SQLite và cấu hình PostgreSQL
SQLITE_DB_PATH = "agno_agi/tmp/6450e752-5391-4561-b0ee-ba1217012b51.db"
def psycopg_connection():
  return psycopg.connect(f"dbname=ai user={posgres_user} password={posgres_password} host=localhost port=5432")


# Kết nối đến PostgreSQL
postgres_engine =create_engine("postgresql+psycopg://", creator=psycopg_connection)
# postgres_engine = create_engine(POSTGRES_DB_URL)
PostgresSession = sessionmaker(bind=postgres_engine)
postgres_session = PostgresSession()

# Kết nối đến SQLite
sqlite_conn = sqlite3.connect(SQLITE_DB_PATH)
sqlite_cursor = sqlite_conn.cursor()

# Tên bảng cần upload/download
TABLE_NAME = "agents_memory"

# Định nghĩa bảng PostgreSQL (nếu chưa tồn tại)
agents_memory_metadata = MetaData()
agents_memory_table = Table(
    "agents_memory",
    agents_memory_metadata,
    Column("id", String, primary_key=True),
    Column("agent_id", String),
    Column("memory_id", String),
    Column("user_id", String),
    Column("memory",  postgresql.JSONB),
    Column("created_at",  DateTime(timezone=True)),
    Column("updated_at", DateTime(timezone=True)),
)
agents_memory_metadata.create_all(postgres_engine)  # Tạo bảng nếu chưa tồn tại
# memory data
#  def get_table(self) -> Table:
#         return Table(
#             self.table_name,
#             self.metadata,
#             Column("id", String, primary_key=True),
#             Column("user_id", String),
#             Column("memory", postgresql.JSONB, server_default=text("'{}'::jsonb")),
#             Column("created_at", DateTime(timezone=True), server_default=text("now()")),
#             Column("updated_at", DateTime(timezone=True), onupdate=text("now()")),
#             extend_existing=True,
#         )
agents_session_metadata = MetaData()
agents_session_table = Table(
    "agents_season",
    agents_session_metadata,
    Column("id", String, primary_key=True),
    Column("agent_id", String),
    Column("session_id", String),
    Column("user_id", String),
    Column("memory",  postgresql.JSONB),
    Column("session_data", postgresql.JSONB),
    Column("extra_data", postgresql.JSONB),
    Column("created_at",  DateTime(timezone=True)),
    Column("updated_at", DateTime(timezone=True)),
)
agents_session_metadata.create_all(postgres_engine)  # Tạo bảng nếu chưa tồn tại
# session data
#  def get_table_v1(self) -> Table:
#         """
#         Define the table schema for version 1.

#         Returns:
#             Table: SQLAlchemy Table object representing the schema.
#         """
#         # Common columns for both agent and workflow modes
#         common_columns = [
#             Column("session_id", String, primary_key=True),
#             Column("user_id", String, index=True),
#             Column("memory", postgresql.JSONB),
#             Column("session_data", postgresql.JSONB),
#             Column("extra_data", postgresql.JSONB),
#             Column("created_at", BigInteger, server_default=text("(extract(epoch from now()))::bigint")),
#             Column("updated_at", BigInteger, server_onupdate=text("(extract(epoch from now()))::bigint")),
#         ]

#         # Mode-specific columns
#         specific_columns = []
#         if self.mode == "agent":
#             specific_columns = [
#                 Column("agent_id", String, index=True),
#                 Column("team_session_id", String, index=True, nullable=True),
#                 Column("agent_data", postgresql.JSONB),
#             ]
#         elif self.mode == "team":
#             specific_columns = [
#                 Column("team_id", String, index=True),
#                 Column("team_session_id", String, index=True, nullable=True),
#                 Column("team_data", postgresql.JSONB),
#             ]
#         elif self.mode == "workflow":
#             specific_columns = [
#                 Column("workflow_id", String, index=True),
#                 Column("workflow_data", postgresql.JSONB),
#             ]

#         # Create table with all columns
#         table = Table(
#             self.table_name,
#             self.metadata,
#             *common_columns,
#             *specific_columns,
#             extend_existing=True,
#             schema=self.schema,  # type: ignore
#         )

#         return table




def upload_sqlite_to_postgres(table : Table,table_name :String,agent_id :String):
    """Upload dữ liệu từ SQLite lên PostgreSQL."""
    # Truy vấn tất cả dữ liệu từ SQLite
    sqlite_cursor.execute(f"SELECT * FROM {table_name}")
    rows = sqlite_cursor.fetchall()

    # Lấy tên cột từ SQLite
    sqlite_cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [col[1] for col in sqlite_cursor.fetchall()]
    columns.append("agent_id")
      # Chuyển dữ liệu lên PostgreSQL với UPSERT
    for row in rows:
        data = dict(zip(columns, list(row) + [agent_id]))  #  # Map tên cột với giá trị
        stmt = insert(table).values(data)
        # Thêm ON CONFLICT để xử lý UPSERT
        stmt = stmt.on_conflict_do_update(
            index_elements=["id"],  # Cột dùng để kiểm tra xung đột (thường là khóa chính)
            set_={col: stmt.excluded[col] for col in data.keys()}  # Cập nhật tất cả các cột
        )
        postgres_session.execute(stmt)
    postgres_session.commit()
    print(f"Đã upload {len(rows)} bản ghi {table_name} từ SQLite lên PostgreSQL.")


# def download_postgres_to_sqlite():
#     """Download dữ liệu từ PostgreSQL về SQLite."""
#     # Truy vấn tất cả dữ liệu từ PostgreSQL
#     result = postgres_session.execute(postgres_table.select()).fetchall()

#     # Xóa dữ liệu cũ trong SQLite
#     sqlite_cursor.execute(f"DELETE FROM {TABLE_NAME}")
#     sqlite_conn.commit()

#     # Lấy tên cột từ PostgreSQL
#     columns = [col.name for col in postgres_table.columns]

#     # Chèn dữ liệu vào SQLite
#     for row in result:
#         data = tuple(row[col] for col in columns)
#         placeholders = ", ".join(["?"] * len(columns))
#         sqlite_cursor.execute(f"INSERT INTO {TABLE_NAME} VALUES ({placeholders})", data)
#     sqlite_conn.commit()
#     print(f"Đã download {len(result)} bản ghi từ PostgreSQL về SQLite.")


# Chạy chương trình
if __name__ == "__main__":
    # Upload dữ liệu từ SQLite lên PostgreSQL
    agent_id ="6450e752-5391-4561-b0ee-ba1217012b51"
    upload_sqlite_to_postgres(agents_memory_table,"agent_memory",agent_id)
    upload_sqlite_to_postgres(agents_session_table,"agent_session",agent_id)
    # Download dữ liệu từ PostgreSQL về SQLite
    # download_postgres_to_sqlite()

# Đóng kết nối
sqlite_conn.close()
postgres_session.close()