import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()
client = OpenAI(
    # This is the default and can be omitted
    # api_key=os.environ.get("OPENAI_API_KEY"),
    api_key = os.getenv("OPENAI_API_KEY"),
)

response = client.responses.create(
    model="gpt-4o",
    instructions="Bạn là hướng dẫn viên du lịch",
    input="Giới thiệu về Hà nội",
)

print(response.output_text)