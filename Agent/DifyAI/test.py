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
    'query': 'trứng có trước hay gà có trước',
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
            
            # Hiển thị Thought ngay khi nhận được
            if json_data.get("event") == "agent_thought":
                thought_text = json_data.get("thought", "")
                if thought_text != full_answer:
                    # Nếu Thought không trùng với Answer thì hiển thị
                    if thought_text:
                        if full_thought == "":
                            print("\n🔹 Bot Thought:", end="", flush=True)
                        full_thought += thought_text
                        print(full_thought, end="", flush=True)  
            # Ghép Answer từng phần và hiển thị ngay
            if json_data.get("event") == "agent_message":
                answer_text = json_data.get("answer", "")
                
                if answer_text:
                    if full_answer == "":
                        print("\n🔹 Bot Answer:", end="", flush=True)
                    full_answer += answer_text
                    print(answer_text, end="", flush=True)  # Hiển thị ngay mà không xuống dòng
                
#             if json_data.get("event") in ["agent_message", "agent_thought"]:
#                 if "answer" in json_data:
#                     full_answer += json_data["answer"]  # Ghép câu trả lời
#                 if "thought" in json_data:
#                     full_thought += json_data["thought"]  # Ghép suy nghĩ (nếu có)
# print("\n🔹 Bot Thought", full_thought)
# print("\n🔹 Bot Answer:", full_answer)  # In toàn bộ câu trả lời đầy đủ