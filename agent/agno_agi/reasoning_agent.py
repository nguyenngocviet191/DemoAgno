from agno.agent import Agent
from agno.cli.console import console
from agno.models.anthropic import Claude
from agno.models.openai import OpenAIChat

task = "Trong xu hướng AI và tự động hóa phát triển, cách kiếm tiền tốt nhất là gì?"

# reasoning_agent_claude = Agent(
#     model=Claude("claude-3-5-sonnet-20241022"),
#     reasoning_model=OpenAIChat(id="o3-mini"),
# )

reasoning_agent_openai = Agent(
    model=OpenAIChat(id="gpt-4o"),
    reasoning_model=OpenAIChat(id="o3-mini"),
)

# console.rule("[bold green]Claude Reasoning Agent[/bold green]")
# reasoning_agent_claude.print_response(task, stream=True)

console.rule("[bold yellow]OpenAI Reasoning Agent[/bold yellow]")
# reasoning_agent_openai.print_response(task, stream=True)
reasoning_agent_openai.print_response(task,show_message=False, stream=True)

res =reasoning_agent_openai.run(
    message="Your message here",
    
)
print(res.content)