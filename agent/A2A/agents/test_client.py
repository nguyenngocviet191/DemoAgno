import asyncio
import sys
import os
path=os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
print(path)
sys.path.append(path)

from common.client.client import A2AClient

async def test_send_task():
    # URL của agent
    agent_url = "http://localhost:10002"

    # Khởi tạo A2AClient
    client = A2AClient(url=agent_url)

    # Payload để gửi tới agent
    payload = {
        "id": "task_id_12345",
        "sessionId": "session_id_67890",
        "acceptedOutputModes": ["text"],
        "message": {
            "role": "user",
            "parts": [
                {
                    "type": "text",
                    "text": "i would claim reimbursement 10 usd for rent car?"
                }
            ]
        }
    }

    # Gửi yêu cầu POST tới agent
    try:
        response = await client.send_task(payload)
        print("Response from agent:", response)
    except Exception as e:
        print("Error:", e)

# Chạy hàm kiểm tra
asyncio.run(test_send_task())