import json
from core.database.database import DatabaseManager
from core.database.utils import db_error_handler


class AIRequestDB:
    def __init__(self):
        self.db_manager = DatabaseManager()

    @db_error_handler
    async def store_ai_request(self, request_data):
        """Stores an AI request in the ai_requests table."""
        print("[DEBUG] Storing AI Request:", json.dumps(request_data, indent=4))

        query = """
            INSERT INTO ai_requests (
                request_name, request_type, request_question, prompt, use_case_id, metadata, created_at
            ) VALUES (
                $1, $2, $3, $4, $5, $6, NOW()
            ) RETURNING id;
        """

        pool = await self.db_manager.get_db_connection()
        async with pool.acquire() as conn:
            async with conn.transaction():
                result = await conn.fetchrow(
                    query,
                    request_data.get("request_name"),
                    request_data.get("request_type"),
                    request_data.get("request_question"),
                    request_data.get("prompt"),  # ✅ Fixed: Now inserting "prompt"
                    request_data.get("use_case_id"),
                    json.dumps(request_data.get("metadata", {})),
                )
                print(
                    "[DEBUG] AI Request Stored with ID:",
                    result["id"] if result else None,
                )
                return result["id"] if result else None

    @db_error_handler
    async def fetch_ai_request(self, request_name):
        """Fetches the AI request for a given request name."""
        print(f"[DEBUG] Fetching AI request with request_name: {request_name}")
        query = "SELECT * FROM ai_requests WHERE request_name = $1 ORDER BY created_at DESC LIMIT 1;"
        pool = await db_manager.get_db_connection()
        async with pool.acquire() as conn:
            result = await conn.fetchrow(query, request_name)
            print("[DEBUG] Fetch AI Request Result:", result)
            return result if result else None


# ✅ Make AIRequestDB importable
ai_request_db = AIRequestDB()
store_ai_request = ai_request_db.store_ai_request
fetch_ai_request = ai_request_db.fetch_ai_request
