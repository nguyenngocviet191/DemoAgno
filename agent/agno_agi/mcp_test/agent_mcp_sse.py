from agno.agent import Agent
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.file import FileTools
from agno.tools.local_file_system import LocalFileSystemTools
from agno.tools.python import PythonTools
from mcp import ClientSession
from  agno.utils.log import log_debug, logger, debug_on
import os
import sys
import logging
# logging.basicConfig(level=logging.DEBUG)

# agno.utils.log.debug_on = True
logging.getLogger("mcp_sse").setLevel(logging.DEBUG)  # Log chi tiết cho thư viện `agno`
logging.getLogger("server_mcp").setLevel(logging.DEBUG)  
add_path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))

# add_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../extended"))
# print(add_path)
sys.path.append(add_path)
from extended.tools.mcp_sse import MCPToolsSSE
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")  # Dùng os.getenv() tránh lỗi KeyError
os.environ["OPENAI_API_KEY"] = api_key
# print(os.getenv("OPENAI_API_KEY"))
mcp_tools = MCPToolsSSE("http://localhost:8000")
# agent = Agent(
#     model=OpenAIChat(id="gpt-4o-mini"),
#     description="Bạn trợ lý hữu ích",
#     # tools=[DuckDuckGoTools(),LocalFileSystemTools()],
#     tools=[mcp_tools],
#     markdown=True,
#     debug_mode=True,
  
# )
# # agent.initialize_agent()
# # # agent.set_agent_id()
# print (agent.tools)
# res= agent.run("nhiệt độ ở Hà Nội hiện tại", stream=False)
# print(res.content)
# print(agent.agent_id)


# agent.print_response("so sánh cổ phiếu FPT và FLC", stream=True,markdown=
#                      True)
# stream = agent.run("xin chào", stream=True)
# for event in stream:
#     print(event.content,end="", flush=True)


