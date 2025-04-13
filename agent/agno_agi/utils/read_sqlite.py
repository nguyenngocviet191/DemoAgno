import sqlite3

# Kết nối đến cơ sở dữ liệu SQLite
conn = sqlite3.connect("agno_agi/tmp/6450e752-5391-4561-b0ee-ba1217012b51.db")
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