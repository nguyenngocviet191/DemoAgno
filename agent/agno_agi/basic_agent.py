from agno.agent import Agent
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")  # Dùng os.getenv() tránh lỗi KeyError
os.environ["OPENAI_API_KEY"] = api_key
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    description="You are an enthusiastic news reporter with a flair for storytelling!",
    markdown=True
)
agent.print_response("Tell me about a breaking news story from New York.", stream=True)