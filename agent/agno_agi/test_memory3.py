from agno.agent.agent import Agent
from agno.memory.v2.db.postgres import PostgresMemoryDb
from agno.memory.v2.memory import Memory
from agno.models.openai import OpenAIChat
from agno.storage.postgres import PostgresStorage
from dotenv import load_dotenv
import os
load_dotenv()
posgres_user = os.getenv("POSTGRES_USER")
posgres_password = os.getenv("POSTGRES_PASSWORD")
db_url = f"postgresql+psycopg://{posgres_user}:{posgres_password}@localhost:5432/ai"

memory = Memory(db=PostgresMemoryDb(table_name="agent_memories", db_url=db_url))

session_id = "postgres_memories"
user_id = "postgres_user"

agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    memory=memory,
    storage=PostgresStorage(table_name="agent_sessions", db_url=db_url),
    enable_user_memories=True,
    enable_session_summaries=True,
)

# agent.print_response(
#     "My name is John Doe and I like to hike in the mountains on weekends.",
#     stream=True,
#     user_id=user_id,
#     session_id=session_id,
# )

agent.print_response(
    "What are my hobbies?", stream=True, user_id=user_id, session_id=session_id
)
print("memories")
print(m for m in agent.memory.get_user_memories(user_id=user_id))
print("session summary")
print(agent.memory.get_session_summary(user_id=user_id, session_id=session_id))
# print(agent.storage.get_all_sessions(user_id=user_id))
print("memories2")
print(m for m in agent.memory.memories)