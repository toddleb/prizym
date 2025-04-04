import asyncio
import json
import logging

from core.database import get_model_responses, save_ai_response
from core.multi_model_controller.arbitration_ai import ArbitrationAI
from core.multi_model_controller.model_router import batch_process_ai_inputs

logger = logging.getLogger(__name__)


async def process_ai_request(request_id: str, prompt: str, models: list):
    """
    Processes an AI request using multiple models and applies arbitration if needed.
    """
    logger.info(f"[AI Processor] Handling request {request_id} with prompt:\n{prompt}")

    responses = []

    for model in models:
        logger.info(f"[AI Processor] Calling {model}...")
        response = await batch_process_ai_inputs(
            [prompt], [model]
        )  # ✅ Properly awaiting
        response_text = response[0] if response else "Error: No response received."

        await save_ai_response(
            request_id, model, response_text
        )  # ✅ Fixed the await issue
        responses.append(response_text)

    # Run arbitration if multiple responses exist
    if len(responses) > 1:
        logger.info(
            f"[Arbitration] Multiple AI responses received. Running arbitration..."
        )
        arbiter = ArbitrationAI()
        final_response = arbiter.run_arbitration(request_id, responses)
    else:
        final_response = responses[0]

    logger.info(f"[AI Processor] Final response selected:\n{final_response}")
    return final_response


# Example Usage
async def main():
    request_id = "test_request_003"
    prompt = "Explain quantum entanglement in simple terms."
    models = ["gpt-4", "mistral-7b", "claude-3"]

    final_response = await process_ai_request(request_id, prompt, models)
    print("\n=== TEST COMPLETE ===")
    print("Final Arbitrated Response:\n", final_response)


if __name__ == "__main__":
    asyncio.run(main())  # ✅ Properly executing async function
