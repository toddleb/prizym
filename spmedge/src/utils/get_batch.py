import json
import re

def extract_clean_json(response_text):
    """Extracts the JSON content from Markdown format."""
    match = re.search(r'```json\n(.*?)\n```', response_text, re.DOTALL)
    return json.loads(match.group(1)) if match else None

def process_batch_results(results_file):
    """Reads batch results and extracts clean JSON data."""
    with open(results_file, "r", encoding="utf-8") as f:
        for line in f:
            response_data = json.loads(line)
            structured_output = extract_clean_json(response_data["response"]["body"]["choices"][0]["message"]["content"])
            
            if structured_output:
                output_filename = f"processed_results_{response_data['custom_id']}.json"
                with open(output_filename, "w", encoding="utf-8") as output_file:
                    json.dump(structured_output, output_file, indent=2)
                print(f"✅ Clean JSON saved to: {output_filename}")

# Run the function
process_batch_results("batch_results_batch_67d7780422448190a4608631067be2c0.jsonl")
