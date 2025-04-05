from agno.agent import Agent
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")  # Dùng os.getenv() tránh lỗi KeyError
os.environ["OPENAI_API_KEY"] = api_key
print(os.getenv("OPENAI_API_KEY"))
agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    description="Bạn là chuyên gia tài chính có nhiều kinh nghiệm thương trường.",
    markdown=True,
  
)
# agent.print_response("so sánh cổ phiếu FPT và FLC", stream=True,markdown=
#                      True)
stream = agent.run("so sánh cổ phiếu và vàng", stream=True)
for event in stream:
    print(event.content,end="", flush=True)