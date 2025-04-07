from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agno.agent import Agent, AgentMemory
from agno.memory.db.postgres import PgMemoryDb
from agno.models.openai import OpenAIChat
from agno.storage.postgres import PostgresStorage
from dotenv import load_dotenv
import os
from uuid import UUID
import logging
load_dotenv()
# Initialize logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

posgres_user = os.getenv("POSTGRES_USER")
posgres_password = os.getenv("POSTGRES_PASSWORD")
openai_api_key = os.getenv("OPENAI_API_KEY")
if not posgres_user or not posgres_password or not openai_api_key:
    logger.error("Missing one or more environment variables (POSTGRES_USER, POSTGRES_PASSWORD, OPENAI_API_KEY).")
app = FastAPI()

class AgentRequest(BaseModel):
    name: str
    introduction: str
@app.post("/create-agent")
def create_agent(req: AgentRequest):
    try:
        db_url = f"postgresql+psycopg://{posgres_user }:{posgres_password}@localhost:5432/ai"
        print(db_url)
        # thêm user&table name để phân theo user
        agent = Agent(
            name=req.name,
            introduction=req.introduction,
            # agent_id = UUID().hex,
            model=OpenAIChat(id="gpt-4o"),
            memory=AgentMemory(
                db=PgMemoryDb(table_name="agent_memory", db_url=db_url),
                create_user_memories=True,
                create_session_summary=True,
            ),
            storage=PostgresStorage(
                table_name="personalized_agent_sessions", db_url=db_url
            ),
            # debug_mode=True,
        )

        return {"status": "ok", "message": f"Agent {agent.name} ({agent.agent_id}) created successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))