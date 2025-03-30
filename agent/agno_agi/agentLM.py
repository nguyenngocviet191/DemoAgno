from agno.agent import Agent, RunResponse
from agno.models.lmstudio import LMStudio
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.file import FileTools
from agno.tools.local_file_system import LocalFileSystemTools
from agno.tools.python import PythonTools

agent = Agent(
    model=LMStudio(id="Hermes-3-Llama-3.2-3B.Q4_K_M.gguf"),
    tools=[DuckDuckGoTools(),LocalFileSystemTools(),PythonTools()],
    markdown=True,
    
)

# Print the response in the terminal
# agent.print_response("Kể một câu về chiến tranh", stream=False,show_message=True)
response = agent.run("xóa các file prime trong thư mục dự án này")    
print(response.content)