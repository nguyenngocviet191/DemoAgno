from typing import Optional, List, cast
# from sqlalchemy import Column
from agno.models.base import Model
from sqlalchemy.types import String, DateTime
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql.expression import text, select
from sqlalchemy.schema import Column, MetaData, Table
from agno.memory.memory import Memory
from agno.memory.db.postgres import PgMemoryDb
from agno.memory.row import MemoryRow
from agno.memory.agent import AgentMemory
from agno.memory.manager import MemoryManager  # Import MemoryManager
from .extended_memory_manager import ExtendedMemoryManager
# from agno.utils.log import logger.debug, logger
from agno.memory.agent import AgentMemory
import logging
# Configure logger
logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
 
# logger.basicConfig(level=logger.DEBUG)
class ExtendedMemoryRow(MemoryRow):
    """Extended MemoryRow to include agent_id."""
    agent_id: Optional[str] = None  # Thêm thuộc tính agent_id

    def to_dict(self) -> dict:
        """Override to_dict to include agent_id."""
        base_dict = super().to_dict()
        base_dict["agent_id"] = self.agent_id
        return base_dict
# class ExtendedMemoryManager(MemoryManager):
#     agent_id: Optional[str] = None  # Thêm thuộc tính agent_id

#     def __init__(self, user_id: Optional[str] = None, db=None, agent_id: Optional[str] = None, **kwargs):
#         super().__init__(user_id=user_id, db=db, **kwargs)
#         self.agent_id = agent_id

#     def get_existing_memories(self) -> Optional[List[ExtendedMemoryRow]]:
#         """Override to filter memories by agent_id."""
#         if self.db is None:
#             return None

#         return self.db.read_memories(user_id=self.user_id, agent_id=self.agent_id, limit=self.limit)

#     def add_memory(self, memory: str) -> str:
#         """Override to include agent_id when adding a memory."""
#         # print("try to add memory")
#         logger.debug("ExtendedMemoryManagertry to add memory")
#         try:
#             if self.db:
#                 self.db.upsert_memory(
#                     ExtendedMemoryRow(
#                         user_id=self.user_id,
#                         agent_id=self.agent_id,  # Thêm agent_id vào dữ liệu
#                         memory=Memory(memory=memory, input=self.input_message).to_dict(),
#                     )
#                 )
#             return "Memory added successfully"
#         except Exception as e:
#             logger.warning(f"Error storing memory in db: {e}")
#             return f"Error adding memory: {e}"

#     def update_memory(self, id: str, memory: str) -> str:
#         """Override to include agent_id when updating a memory."""
#         logger.debug("ExtendedMemoryManager try to update memory")
#         try:
#             if self.db:
#                 self.db.upsert_memory(
#                     ExtendedMemoryRow(
#                         id=id,
#                         user_id=self.user_id,
#                         agent_id=self.agent_id,  # Thêm agent_id vào dữ liệu
#                         memory=Memory(memory=memory, input=self.input_message).to_dict(),
#                     )
#                 )
#             logger.debug("Memory updated successfully")    
#             return "Memory updated successfully"
#         except Exception as e:
#             logger.warning(f"Error updating memory in db: {e}")
#             return f"Error updating memory: {e}"
#     def add_tools_to_model(self, model: Model) -> None:
#         super().add_tools_to_model(model) 

class ExtendedAgentMemory(AgentMemory):
    agent_id: Optional[str] = None  # Thêm thuộc tính agent_id
    def __init__(self, user_id: str, db=None, agent_id: str = None, **kwargs):
        super().__init__(user_id=user_id, db=db, **kwargs)
        self.agent_id = agent_id  # Thêm thuộc tính agent_id

    def to_dict(self) -> dict:
        """Override to_dict to include agent_id."""
        base_dict = super().to_dict()
        base_dict["agent_id"] = self.agent_id
        return base_dict

    def update_memory(self, input: str, force: bool = False) -> Optional[str]:
        """Override update_memory to include agent_id in memory data."""
        logger.debug("ExtendedAgentMemory try update memory")
        if self.db is None:
            logger.warning("MemoryDb not provided.")
            return "Please provide a db to store memories"

        self.updating_memory = True

        # Check if this user message should be added to long-term memory
        should_update_memory = force or self.should_update_memory(input=input)
        logger.debug(f"Update memory: {should_update_memory}")

        if not should_update_memory:
            logger.debug("Memory update not required")
            return "Memory update not required"
        # self.manager = ExtendedMemoryManager(user_id=self.user_id,agent_id=self.agent_id, db=self.db)
        # self.manager.add_memory("This is a test memory")
        if self.manager is None:
            self.manager = ExtendedMemoryManager(user_id=self.user_id,agent_id=self.agent_id, db=self.db)

        else:
            self.manager.db = self.db
            self.manager.agent_id = self.agent_id
            self.manager.user_id = self.user_id
        logger.debug(f"Class name: {self.manager.__class__.__name__}")
        # self.manager.add_memory("This is a test memory 3")
        # Include agent_id in the memory update process
        logger.debug("ExtendedAgentMemory try running memory manager")
        self.manager = cast(ExtendedMemoryManager, self.manager)
        # self.manager.add_memory("This is a test memory 3")
        response = self.manager.run(input)
        # response = "test memory"
        # logger.debug(f"response {response}")
        self.load_user_memories()
        self.updating_memory = False
        return response
    
class ExtendedPgMemoryDb(PgMemoryDb):
   
    def get_table(self):
        """Override to add the agent_id column."""
        return Table(
            self.table_name,
            self.metadata,
            Column("id", String, primary_key=True),
            Column("user_id", String),
            Column("agent_id", String),  # Thêm cột agent_id
            Column("memory", postgresql.JSONB, server_default=text("'{}'::jsonb")),
            Column("created_at", DateTime(timezone=True), server_default=text("now()")),
            Column("updated_at", DateTime(timezone=True), onupdate=text("now()")),
            extend_existing=True,
        )

    def read_memories(
        self, user_id: Optional[str] = None,  agent_id: Optional[str] = None, limit: Optional[int] = None, sort: Optional[str] = None
    ) -> List[ExtendedMemoryRow]:
        """Override to support filtering by agent_id."""
        memories: List[ExtendedMemoryRow] = []
        try:
            with self.Session() as sess, sess.begin():
                stmt = select(self.table)
                if user_id is not None:
                    stmt = stmt.where(self.table.c.user_id == user_id)
                if agent_id is not None:
                    stmt = stmt.where(self.table.c.agent_id == agent_id)
                if limit is not None:
                    stmt = stmt.limit(limit)

                if sort == "asc":
                    stmt = stmt.order_by(self.table.c.created_at.asc())
                else:
                    stmt = stmt.order_by(self.table.c.created_at.desc())

                rows = sess.execute(stmt).fetchall()
                for row in rows:
                    if row is not None:
                        memories.append(ExtendedMemoryRow.model_validate(row))
        except Exception as e:
            logger.debug(f"Exception reading from table: {e}")
            logger.debug(f"Table does not exist: {self.table.name}")
            logger.debug("Creating table for future transactions")
            self.create()
        return memories

    def upsert_memory(self, memory: ExtendedMemoryRow, create_and_retry: bool = True) -> None:
        """Override to include agent_id in the upsert."""
        try:
            with self.Session() as sess, sess.begin():
                # Create an insert statement
                stmt = postgresql.insert(self.table).values(
                    id=memory.id,
                    user_id=memory.user_id,
                    agent_id=memory.agent_id,  # Thêm agent_id vào dữ liệu
                    memory=memory.memory,
                )

                # Define the upsert if the memory already exists
                stmt = stmt.on_conflict_do_update(
                    index_elements=["id"],
                    set_=dict(
                        user_id=stmt.excluded.user_id,
                        agent_id=stmt.excluded.agent_id,  # Cập nhật agent_id nếu tồn tại
                        memory=stmt.excluded.memory,
                    ),
                )

                sess.execute(stmt)
        except Exception as e:
            logger.debug(f"Exception upserting into table: {e}")
            logger.debug(f"Table does not exist: {self.table.name}")
            logger.debug("Creating table for future transactions")
            self.create()
            if create_and_retry:
                return self.upsert_memory(memory, create_and_retry=False)
            return None