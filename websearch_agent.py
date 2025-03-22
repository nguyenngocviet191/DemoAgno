from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")  # Dùng os.getenv() tránh lỗi KeyError
os.environ["OPENAI_API_KEY"] = api_key
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    tools=[DuckDuckGoTools()],
    markdown=True
)
agent.print_response("Chuyện gì xảy ra ở Hà nội hôm nay", stream=True)