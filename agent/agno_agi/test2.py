import os

api_key = os.getenv("OPENAI_API_KEY")  # Dùng os.getenv() tránh lỗi KeyError
print ("API key: ", api_key)
if api_key:
    print("API key đã được thiết lập:", api_key)
else:
    print("API key chưa được thiết lập hoặc rỗng!")