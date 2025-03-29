import requests
import os
from dotenv import load_dotenv
import json
# Load environment variables from a .env file


# Ví dụ dữ liệu chunk nhận được
load_dotenv()

# Thay thế bằng API Key của bạn
api_key = os.getenv("difyai_api_key")
api_url = 'https://api.dify.ai/v1/chat-messages'

headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json',
    'Accept': 'text/event-stream',
}

# Dữ liệu gửi đến API
payload = {
    'inputs': {},  # Thay thế bằng các biến đầu vào nếu cần
    'query': 'giải thích về crypto',
    'response_mode': "streaming",  # Hoặc 'streaming' nếu bạn muốn nhận kết quả theo luồng
    'conversation_id': '',  # Để trống khi bắt đầu cuộc trò chuyện mới
    'user': 'shin-test'  # Thay thế bằng ID người dùng của bạn
}


chunk_example = b'data: {"event": "message", "answer": "Hi"}\n\n'

response = requests.post(api_url, headers=headers, json=payload, stream=True)
full_answer = ""
full_thought = ""

for line in response.iter_lines():
    if line:
        line = line.decode("utf-8").strip()
        if line.startswith("data: "):
            json_data = json.loads(line.replace("data: ", ""))
            
            # Lấy dữ liệu từ "agent_message" hoặc "agent_thought"
            if json_data.get("event") in ["agent_message", "agent_thought"]:
                if "answer" in json_data:
                    full_answer += json_data["answer"]  # Ghép câu trả lời
                if "thought" in json_data:
                    full_thought += json_data["thought"]  # Ghép suy nghĩ (nếu có)
print("\n🔹 Bot Thought", full_thought)
print("\n🔹 Bot Answer:", full_answer)  # In toàn bộ câu trả lời đầy đủ