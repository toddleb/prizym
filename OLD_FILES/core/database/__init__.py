from core.database.database import db_manager
from core.database.db_ai_request import AIRequestDB
from core.database.db_ai_response import AIResponseDB

# ✅ Initialize database instances
get_db_connection = db_manager.get_db_connection

ai_request_db = AIRequestDB()
ai_response_db = AIResponseDB()

__all__ = ["db_manager", "get_db_connection", "ai_request_db", "ai_response_db"]
