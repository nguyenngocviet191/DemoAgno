from agno.memory.agent import AgentMemory
from agno.memory.db.postgres import PgMemoryDb
from agno.memory.memory import Memory
from lib.memory import ExtendedPgMemoryDb ,ExtendedAgentMemory

from sqlalchemy import create_engine
import uuid
from dotenv import load_dotenv
import os
import logging
# Configure logger
logging.basicConfig(level=logging.INFO) 
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("memory").setLevel(logging.WARNING)
logging.getLogger("extended_memory_manager").setLevel(logging.WARNING)
load_dotenv()
posgres_user = os.getenv("POSTGRES_USER")
posgres_password = os.getenv("POSTGRES_PASSWORD")
DB_URL = f"postgresql+psycopg://{posgres_user}:{posgres_password}@localhost:5432/ai"
# print(DB_URL)
# Cấu hình kết nối đến PostgreSQL
# DB_URL = "postgresql://username:password@localhost:5432/agent_memory_db"

# Khởi tạo cơ sở dữ liệu PostgreSQL
db_engine = create_engine(DB_URL)
memory_db=ExtendedPgMemoryDb(table_name="multi_agent_memory2", db_url=DB_URL,schema="ai")
# memory_db = PgMemoryDb(
#     table_name="agent_memories",
#     db_url=DB_URL,
#     schema="public",  # Sử dụng schema mặc định
#     db_engine=db_engine,
# )

# Tạo agent đầu tiên
# agent1_id = str(uuid.uuid4())  # Tạo ID duy nhất cho agent 1
# print(f"Created agent {agent1_id}")
# agent1_id ="eac822da-1207-464f-9c40-d2c4077cad70"
# agent1_memory = ExtendedAgentMemory(
#     user_id="user_1",
#     agent_id = agent1_id,
#     db=memory_db,
# )
# agent1_memory.update_memory(f"Tôi muốn làm việc với kĩ sư AI", force=True)
# agent1_memory = ExtendedAgentMemory(
#     user_id="user_2",
#     agent_id = agent1_id,
#     db=memory_db,
# )
# agent1_memory.update_memory(f"Tôi là họ sỹ", force=True)

agent2_id = str(uuid.uuid4())
print(f"Created agent {agent2_id}")
agent2_memory = ExtendedAgentMemory(
    user_id="user_1",
    agent_id = agent2_id,
    db=memory_db,
)
agent2_memory.update_memory(f"Hôm qua tôi đi bơi", force=True)


# Truy vấn và hiển thị dữ liệu từ cơ sở dữ liệu
def display_memories(agent_memory: ExtendedAgentMemory, agent_id: str):
    print(f"Memories for Agent {agent_id}:")
    agent_memory.load_user_memories()
    for memory in agent_memory.memories:
        print(memory.to_dict())

# Hiển thị bộ nhớ của Agent 1
# display_memories(agent1_memory, agent1_id)
display_memories(agent2_memory, agent2_id)
# # Hiển thị bộ nhớ của Agent 2
# display_memories(agent2_memory, agent2_id)
# print("done")