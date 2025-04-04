import asyncio
from enum import Enum
from typing import Any, Dict, Set

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

import ai.workflow_engine as workflow_engine  # ✅ Import module instead of function
from core.registries.model_registry import get_registered_model
from core.registries.phase_registry import get_phase_sequence

app = FastAPI()
active_connections: Set[WebSocket] = set()


class WorkflowPhase(Enum):
    INPUT = ("1", "Input Data Processing")
    PREPROCESSING = ("2", "Data Preprocessing")
    AI_EXECUTION = ("3", "AI Execution")
    VALIDATION = ("4", "Results Validation")
    OUTPUT = ("5", "Output Generation")

    def __init__(self, node_id: str, description: str):
        self.node_id = node_id
        self.description = description


async def send_phase_update(
    websocket: WebSocket, phase: WorkflowPhase, is_starting: bool = True
):
    """Send phase status update to the client."""
    await websocket.send_json(
        {
            "nodeId": phase.node_id,
            "logMessage": f"{'Starting' if is_starting else 'Completed'} {phase.description} {'...' if is_starting else '✅'}",
        }
    )


async def handle_workflow_execution(websocket: WebSocket, input_data: dict):
    """Handle the AI workflow execution with detailed progress updates."""
    try:
        # Input phase
        await send_phase_update(websocket, WorkflowPhase.INPUT)
        model = get_registered_model("default_model")
        phase_sequence = get_phase_sequence()
        await asyncio.sleep(1)  # Simulate input processing
        await send_phase_update(websocket, WorkflowPhase.INPUT, False)

        # Preprocessing phase
        await send_phase_update(websocket, WorkflowPhase.PREPROCESSING)
        await asyncio.sleep(1.5)
        await send_phase_update(websocket, WorkflowPhase.PREPROCESSING, False)

        # AI Execution phase
        await send_phase_update(websocket, WorkflowPhase.AI_EXECUTION)
        result = await workflow_engine.execute_workflow(  # ✅ Fix function call
            input_data=input_data, model=model, phase_sequence=phase_sequence
        )
        await send_phase_update(websocket, WorkflowPhase.AI_EXECUTION, False)

        # Validation phase
        await send_phase_update(websocket, WorkflowPhase.VALIDATION)
        await asyncio.sleep(1)
        await send_phase_update(websocket, WorkflowPhase.VALIDATION, False)

        # Output phase
        await send_phase_update(websocket, WorkflowPhase.OUTPUT)
        final_result = {
            "execution_result": result,
            "status": "success",
            "timestamp": "timestamp_here",
        }
        await asyncio.sleep(0.5)
        await send_phase_update(websocket, WorkflowPhase.OUTPUT, False)

        # ✅ Ensure AI results are properly sent back
        await websocket.send_json(
            {"nodeId": "5", "logMessage": "AI Output Ready", "data": final_result}
        )

        return final_result

    except Exception as e:
        await websocket.send_json(
            {
                "nodeId": "error",
                "logMessage": f"Error in workflow execution: {str(e)}",
                "error": str(e),
            }
        )
        raise


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handle WebSocket connections and workflow execution."""
    await websocket.accept()
    active_connections.add(websocket)
    print("✅ WebSocket Connected!")

    try:
        while True:
            data = await websocket.receive_json()
            print(f"📩 Received from client: {data}")

            if data.get("action") == "process":
                try:
                    result = await handle_workflow_execution(
                        websocket=websocket, input_data=data.get("data", {})
                    )

                except Exception as e:
                    print(f"Error in workflow: {e}")
                    await websocket.send_json(
                        {
                            "nodeId": "error",
                            "logMessage": f"Workflow failed: {str(e)}",
                            "error": str(e),
                        }
                    )

    except WebSocketDisconnect:
        print("❌ WebSocket Disconnected.")
    finally:
        active_connections.remove(websocket)
        print("Connection cleaned up")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=3300, log_level="debug")
