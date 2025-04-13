import sqlite3

# Kết nối đến cơ sở dữ liệu SQLite
conn = sqlite3.connect("agno_agi/tmp/b5398dae-a482-4a23-a717-6616c2f84fe8.db")
cursor = conn.cursor()
# Truy vấn danh sách các bảng
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# Lấy tất cả kết quả
tables = cursor.fetchall()
print("Danh sách các bảng trong cơ sở dữ liệu:")
for table in tables:
    print(table[0])
# Thực thi câu truy vấn
cursor.execute("SELECT * FROM agent_memory")

# Lấy tất cả kết quả
rows = cursor.fetchall()

# In ra kết quả
for row in rows:
    print(row)

# Đóng kết nối
conn.close()