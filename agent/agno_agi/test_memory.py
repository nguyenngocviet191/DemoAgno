from agno.agent import Agent, AgentMemory
from agno.memory.db.postgres import PgMemoryDb
from agno.models.openai import OpenAIChat
from agno.storage.postgres import PostgresStorage
from rich.pretty import pprint
from dotenv import load_dotenv
import os
load_dotenv()
posgres_user = os.getenv("POSTGRES_USER")
posgres_password = os.getenv("POSTGRES_PASSWORD")

db_url = f"postgresql+psycopg://{posgres_user}:{posgres_password}@localhost:5432/ai"
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    # Store the memories and summary in a database
    memory=AgentMemory(
        db=PgMemoryDb(table_name="agent_memory", db_url=db_url),
        create_user_memories=True,
        create_session_summary=True,
    ),
    # Store agent sessions in a database
    storage=PostgresStorage(
        table_name="personalized_agent_sessions", db_url=db_url
    ),
    # Show debug logs so, you can see the memory being created
    # debug_mode=True,
)

# -*- Share personal information
agent.print_response("Tôi là Việt", stream=True)
# -*- Print memories
pprint(agent.memory.memories)
# -*- Print summary
pprint(agent.memory.summary)

# -*- Share personal information
agent.print_response("Tôi sống ở Hà nội", stream=True)
# -*- Print memories
pprint(agent.memory.memories)
# -*- Print summary
pprint(agent.memory.summary)

# -*- Share personal information
agent.print_response("Tôi là developer", stream=True)
# -*- Print memories
pprint(agent.memory.memories)
# -*- Print summary
pprint(agent.memory.summary)

# Ask about the conversation
agent.print_response(
    "Bạn có nhớ thông tin gì về tôi không", stream=True
)
pprint(agent.agent_id)