from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import os
from openai import OpenAI

# Khởi tạo FastAPI
app = FastAPI()

# Set the API key for OpenAI
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Hàm stream response từ OpenAI
# async def stream_chat_response(prompt: str):
#     response = await openai_client.chat.completions.create(
#         model="gpt-4",
#         messages=[{"role": "user", "content": prompt}],
#         stream=True,  # Bật chế độ stream
#     )

#     async for chunk in response:
#         if chunk.choices and chunk.choices[0].delta:
#             yield chunk.choices[0].delta.content

# # API nhận tin nhắn từ user và trả lời dạng stream
# @app.post("/chat")
import openai

# Set the API key for OpenAI
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

stream = client.responses.create(
    model="gpt-4o-mini",
    input=[{"role": "user", "content": "so sánh cổ phiếu và crypto"}],
    stream=True  # Enable streaming
)
# print(response.choices[0].message.content)
for event in stream:
    print(event)
# for chunk in response:
#     if "message" in chunk and "message" in chunk["choices"][0]:
#         print(chunk["choices"][0]["message"]["content"], end="", flush=True)

# for chunk in response:
#     if chunk.choices and chunk.choices[0].delta:
#         yield chunk.choices[0].delta.content