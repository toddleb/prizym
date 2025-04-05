import openai
import json
from pathlib import Path

def retrieve_results(batch_id, output_file_id):
    """Downloads and saves batch results to stage_process directory."""
    try:
        # Define the correct directory
        stage_process_dir = Path("/Users/toddlebaron/prizym/spmedge/data/stage_process")
        stage_process_dir.mkdir(parents=True, exist_ok=True)  # Ensure directory exists

        file_response = openai.files.content(output_file_id)

        # Read and decode the binary content
        results = file_response.read().decode("utf-8")

        # Save the results in stage_process directory
        output_filename = stage_process_dir / f"batch_results_{batch_id}.jsonl"
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(results)

        print(f"✅ Batch results saved: {output_filename}")
        return output_filename

    except Exception as e:
        print(f"❌ Failed to retrieve results for batch {batch_id}: {e}")
        return None

# Run retrieval function
retrieve_results("batch_67d7b004612c819083461b8708b4ed5e", "file-DmXonBy4cYGAyEWTAuA6Bn")
