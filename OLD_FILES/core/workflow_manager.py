import asyncio
import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict

from core.database import (
    db_manager,
)  # ✅ Use db_manager instead of raw get_db_connection()
from core.database.db_ai_response import (
    ai_response_db,
)  # ✅ Ensure AI response storage is used
from core.loopback.loopback import loopback_manager
from core.multi_model_controller.model_router import batch_process_ai_inputs

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class WorkflowManager:
    """Centralized AI Workflow Execution with Dynamic Model Selection & Loopback."""

    def __init__(self):
        self.setup_complete = False

    async def ensure_setup(self):
        """Ensure database tables and constraints are properly set up."""
        if self.setup_complete:
            return

        conn = await db_manager.get_db_connection()
        try:
            await conn.execute("DROP TABLE IF EXISTS model_performance;")
            await conn.execute(
                """
                CREATE TABLE model_performance (
                    id SERIAL PRIMARY KEY,
                    model_id UUID NOT NULL REFERENCES ai_models(id),
                    success_rate FLOAT DEFAULT 1.0,
                    average_latency FLOAT DEFAULT 0.0,
                    total_executions INT DEFAULT 0,
                    successful_executions INT DEFAULT 0,
                    last_updated TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(model_id)
                );
            """
            )

            self.setup_complete = True
        finally:
            await conn.close()

    async def execute_workflow(self, workflow_name: str, request_id: int):
        """Execute a workflow dynamically by fetching its phases and AI actions."""
        await self.ensure_setup()
        conn = await db_manager.get_db_connection()

        try:
            workflow = await conn.fetchrow(
                "SELECT id FROM workflows WHERE name = $1", workflow_name
            )
            if not workflow:
                logger.error(f"❌ Workflow '{workflow_name}' not found.")
                return

            workflow_id = workflow["id"]
            phases = await conn.fetch(
                """
                SELECT id, phase_name, phase_number
                FROM phases 
                WHERE workflow_type_id = $1 
                ORDER BY phase_number
                """,
                workflow_id,
            )

            if not phases:
                logger.error(f"❌ No phases found for workflow '{workflow_name}'.")
                return

            workflow_context = {}
            for phase in phases:
                phase_id = phase["id"]
                phase_name = phase["phase_name"]

                logger.info(f"🚀 Executing phase: {phase_name}")

                model_info = await self.select_best_model(phase_id)
                if not model_info:
                    logger.warning(f"⚠️ No AI models found for phase '{phase_name}'")
                    continue

                action_name = model_info["action_name"]
                model_name = model_info["model_name"].strip()

                if not model_name.replace("-", "").isalnum():
                    logger.error(
                        f"🚨 Invalid model name detected: {model_name}. Skipping execution."
                    )
                    continue

                logger.info(f"🛠 Executing action: {action_name} using {model_name}")

                start_time = datetime.now(timezone.utc)
                try:
                    prompt = self.prepare_prompt(action_name, workflow_context)

                    # 🚀 Debug: Confirm the AI model is being called
                    print(
                        f"[DEBUG] Calling AI Model: {model_name} with input: {prompt}"
                    )

                    print(
                        f"[DEBUG] Calling AI Model: {model_name} with input: {prompt}"
                    )
                    ai_response = await batch_process_ai_inputs([prompt], [model_name])
                    print(f"[DEBUG] AI Model Response: {ai_response}")

                    if not ai_response or (
                        isinstance(ai_response, list) and not ai_response[0]
                    ):
                        print(
                            "🚨 [ERROR] AI Model did NOT return a valid response! Skipping storage."
                        )
                        continue  # Prevents storing an empty response

                    # 🚀 Debug: Log AI response
                    print(f"[DEBUG] AI Model Response: {ai_response}")

                    if isinstance(ai_response, list):
                        ai_response = ai_response[0] if ai_response else ""

                    execution_time = (
                        datetime.now(timezone.utc) - start_time
                    ).total_seconds()
                    success = isinstance(ai_response, str) and len(ai_response) > 5

                    await self.log_model_performance_with_retry(
                        model_name, execution_time, success
                    )

                    # ✅ Store AI Response in Database
                    response_data = {
                        "model_name": model_name,
                        "input_text": prompt,
                        "response": ai_response,
                        "request_id": request_id,
                        "metadata": {"phase": phase_name, "workflow_id": workflow_id},
                    }
                    print(
                        f"[DEBUG] Storing AI Response: {json.dumps(response_data, indent=4)}"
                    )
                    response_id = await ai_response_db.store_ai_response(response_data)
                    print(f"[DEBUG] AI Response Stored with ID: {response_id}")

                    workflow_context[phase_name] = {
                        "response": ai_response,
                        "model": model_name,
                        "success": success,
                    }

                    try:
                        # Update loopback call to match the expected API
                        refined_response = await loopback_manager.refine_response(
                            workflow_id, phase_id, ai_response
                        )

                        if refined_response and refined_response != ai_response:
                            workflow_context[phase_name]["response"] = refined_response
                            logger.info(
                                f"🔄 Loopback improved response for '{action_name}'"
                            )
                        else:
                            logger.info(
                                f"⚠️ Loopback did NOT modify response for '{action_name}'"
                            )
                    except Exception as e:
                        logger.error(
                            f"🚨 Loopback error in phase '{phase_name}': {str(e)}"
                        )

                except Exception as e:
                    logger.error(f"🚨 Error in phase '{phase_name}': {str(e)}")
                    continue

            logger.info(f"✅ Workflow '{workflow_name}' executed successfully!")
            return workflow_context

        except Exception as e:
            logger.error(f"🚨 Error executing workflow '{workflow_name}': {str(e)}")
            return None
        finally:
            await conn.close()

    async def select_best_model(self, phase_id: str):
        """Select the best AI model dynamically based on past execution performance."""
        conn = await db_manager.get_db_connection()
        try:
            model = await conn.fetchrow(
                """
                SELECT ma.action_name, am.model_name
                FROM model_action_library ma
                JOIN ai_models am ON ma.model_id = am.id
                LEFT JOIN model_performance mp ON ma.model_id = mp.model_id
                WHERE ma.phase_id = $1
                ORDER BY 
                    COALESCE(mp.success_rate, 1.0) DESC, 
                    COALESCE(mp.average_latency, 9999) ASC
                LIMIT 1;
                """,
                phase_id,
            )
            return model if model else None
        finally:
            await conn.close()

    def prepare_prompt(self, action_name: str, context: Dict[str, Any]) -> str:
        """Prepare context-aware prompt for the AI model."""
        return action_name


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run a specific workflow.")
    parser.add_argument(
        "workflow_name", type=str, help="The name of the workflow to execute"
    )
    parser.add_argument(
        "request_id", type=int, help="The request ID associated with the workflow"
    )

    args = parser.parse_args()

    manager = WorkflowManager()
    asyncio.run(manager.execute_workflow(args.workflow_name, args.request_id))
