import json
import uuid
from core.database.database import DatabaseManager
from core.database.utils import db_error_handler


class AIModelDB:
    def __init__(self):
        self.db_manager = DatabaseManager()

    @db_error_handler
    async def create_ai_model(self, model_data):
        query = """
            INSERT INTO ai_models (
                id, model_name, provider, capabilities, performance_score, status, 
                created_at, parameters, category, use_cases, api_endpoint, version,
                cost_per_token, latency, token_limit, dependencies, owner
            ) VALUES (
                $1, $2, $3, $4, $5, $6, NOW(), $7, $8, $9, $10, $11, $12, $13, $14, $15, $16
            ) RETURNING id;
        """
        model_id = uuid.uuid4()
        pool = await db_manager.get_db_connection()
        async with pool.acquire() as conn:
            async with conn.transaction():
                result = await conn.fetchrow(
                    query,
                    model_id,
                    model_data.get("model_name"),
                    model_data.get("provider"),
                    json.dumps(model_data.get("capabilities", {})),
                    model_data.get("performance_score", 0.0),
                    model_data.get("status", "active"),
                    json.dumps(model_data.get("parameters", {})),
                    model_data.get("category"),
                    json.dumps(model_data.get("use_cases", [])),
                    model_data.get("api_endpoint"),
                    model_data.get("version", "1.0"),
                    model_data.get("cost_per_token", 0.0),
                    model_data.get("latency", 0.0),
                    model_data.get("token_limit", 0),
                    json.dumps(model_data.get("dependencies", {})),
                    model_data.get("owner"),
                )
                return result["id"] if result else None
