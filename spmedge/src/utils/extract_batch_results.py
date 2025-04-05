import json
from pathlib import Path

def parse_batch_results(results_file):
    """Parses and processes each document in the batch results."""
    results_path = Path(results_file)

    if not results_path.exists():
        print(f"❌ File not found: {results_file}")
        return

    with open(results_file, "r", encoding="utf-8") as f:
        for line in f:
            try:
                result = json.loads(line.strip())  # Load JSON from each line
                doc_id = result.get("custom_id")  # Get document ID
                structured_output = result.get("response", {}).get("body", {}).get("choices", [{}])[0].get("message", {}).get("content", "")

                if structured_output:
                    print(f"\n✅ Document ID: {doc_id}")
                    print("📄 Extracted Structured Data:")
                    print(structured_output[:500])  # Print first 500 chars
                else:
                    print(f"⚠️ No structured data found for {doc_id}")

            except json.JSONDecodeError as e:
                print(f"❌ JSON parsing error: {e}")

# Run function with the correct file name
parse_batch_results("/Users/toddlebaron/prizym/spmedge/data/stage_process/batch_results_batch_67d7b004612c819083461b8708b4ed5e.jsonl")
