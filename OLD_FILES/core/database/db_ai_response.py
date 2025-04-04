import json
import logging
from core.database import db_manager
from core.database.utils import db_error_handler

logger = logging.getLogger(__name__)


class AIResponseDB:
    def __init__(self):
        self.db_manager = db_manager

    @db_error_handler
    async def store_ai_response(self, response_data):
        """Stores an AI-generated response in the ai_responses table."""
        print("[DEBUG] Storing AI Response:", json.dumps(response_data, indent=4))

        query = """
            INSERT INTO ai_responses (
                model_name, input_text, response, metadata, created_at, request_id
            ) VALUES (
                $1, $2, $3, $4, NOW(), $5
            ) RETURNING id;
        """

        pool = await self.db_manager.get_db_connection()
        async with pool.acquire() as conn:
            async with conn.transaction():
                result = await conn.fetchrow(
                    query,
                    response_data.get("model_name"),
                    response_data.get("input_text"),
                    response_data.get("response"),
                    json.dumps(response_data.get("metadata", {})),
                    response_data.get("request_id"),
                )
                response_id = result["id"] if result else None
                print(f"[DEBUG] AI Response Stored with ID: {response_id}")
                return response_id

    @db_error_handler
    async def fetch_ai_response(self, request_id, input_text):
        """Fetches the AI-generated response for a given input_text."""
        print(
            f"[DEBUG] Fetching AI response with request_id: {request_id}, input_text: {input_text}"
        )

        query = """
            SELECT * FROM ai_responses
            WHERE request_id = $1 AND input_text = $2
            ORDER BY created_at DESC LIMIT 1;
        """

        pool = await self.db_manager.get_db_connection()
        async with pool.acquire() as conn:
            result = await conn.fetchrow(query, request_id, input_text)
            print("[DEBUG] Fetch AI Response Result:", result)
            return dict(result) if result else None


# ✅ Make AIResponseDB importable
ai_response_db = AIResponseDB()
