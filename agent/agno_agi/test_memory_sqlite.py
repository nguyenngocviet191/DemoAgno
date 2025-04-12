import json
import uuid
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.storage.sqlite import SqliteStorage
from agno.memory.db.sqlite import SqliteMemoryDb
from agno.memory import AgentMemory
from rich.console import Console
from rich.json import JSON
from rich.panel import Panel
from pathlib import Path
import copy
# ************* Setup Paths *************
# Define the current working directory
cwd = Path(__file__).parent
# Create a tmp directory for storing agent sessions and knowledge
tmp_dir = cwd.joinpath("tmp")
tmp_dir.mkdir(parents=True, exist_ok=True)

agent_id = "b5398dae-a482-4a23-a717-6616c2f84fe8"
# agent_id = str(uuid.uuid4())
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    # Store agent sessions in a database
    agent_id =agent_id,
    memory=AgentMemory(
        db =SqliteMemoryDb(
            table_name="agent_memory", db_file=str(tmp_dir.joinpath(f"{agent_id}.db"))),    
        create_user_memories=True,
        create_session_summary=True,
    ),
    storage=SqliteStorage(
        table_name="agent_sessions", db_file=str(tmp_dir.joinpath(f"{agent_id}.db")) ),
    # Set add_history_to_messages=true to add the previous chat history to the messages sent to the Model.
    add_history_to_messages=True,
    # Number of historical responses to add to the messages.
    num_history_responses=3,
    # The session_id is used to identify the session in the database
    # You can resume any session by providing a session_id
    # session_id="xxxx-xxxx-xxxx-xxxx",
    # Description creates a system prompt for the agent
    description="You are a helpful assistant that always responds in a polite, upbeat and positive manner.",
)
# res = agent.run("Tôi là ai")
# print(res.content)
# for m in agent.memory.messages:

agent.update_memory("Tôi sống ở Hà nội")
res = agent.memory.db.get_table()

print(res)
# agent2.storage.u