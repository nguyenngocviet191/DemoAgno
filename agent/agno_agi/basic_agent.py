from agno.agent import Agent
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.file import FileTools
from agno.tools.local_file_system import LocalFileSystemTools
from agno.tools.python import PythonTools
import os
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")  # Dùng os.getenv() tránh lỗi KeyError
os.environ["OPENAI_API_KEY"] = api_key
# print(os.getenv("OPENAI_API_KEY"))
agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    description="Bạn là chuyên gia tài chính có nhiều kinh nghiệm thương trường.",
    tools=[DuckDuckGoTools(),LocalFileSystemTools()],
    markdown=True,
    debug_mode=True,
  
)
agent.initialize_agent()
# # agent.set_agent_id()
# res= agent.run("so sánh cổ phiếu và vàng", stream=False)

print(agent.agent_id)
print (agent.tools)
# print(res.content)
# agent.print_response("so sánh cổ phiếu FPT và FLC", stream=True,markdown=
#                      True)
# stream = agent.run("xin chào", stream=True)
# for event in stream:
#     print(event.content,end="", flush=True)

print(agent.memory.messages)