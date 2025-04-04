import json
import logging
from database import get_spm_framework
from spm_matcher import match_spm_tags

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def analyze_comp_plan(cleaned_text, schema):
    """Extract and structure compensation plan data."""
    logging.info("🔹 Extracting compensation components...")

    # Load the SPM knowledge framework
    spm_framework = get_spm_framework()

    # Extracted comp plan structure
    processed_data = {
        "plan_title": schema.get("plan_title", "Unknown Plan"),
        "effective_dates": schema.get("effective_dates", {}),
        "plan_summary": {
            "text": cleaned_text[:500],  # Capture first 500 chars for summary
            "keywords": [],
            "client_tags": {}
        },
        "compensation_structure": {},
        "payout_schedule": {},
        "special_provisions": [],
        "terms_and_conditions": []
    }

    # Extract key components (Placeholder - Replace with actual NLP logic)
    components = [
        {"name": "Quota Bonus", "type": "Bonus", "amount": "$10,000"},
        {"name": "MBO Bonus", "type": "Bonus", "amount": "$5,000"},
        {"name": "Recoverable Draw", "type": "Draw", "amount": "Varies"}
    ]

    for comp in components:
        matched_tags = match_spm_tags(comp["name"], spm_framework)
        processed_data["compensation_structure"][comp["name"]] = {
            "component_type": matched_tags.get("component", "Unknown"),
            "details": {
                "type": comp["type"],
                "target_amount": comp["amount"],
                "payout_frequency": "Quarterly"
            },
            "keywords": matched_tags.get("keywords", [])
        }

    # Extract payout schedule (Placeholder logic)
    processed_data["payout_schedule"] = {
        "description": "Payouts are made quarterly based on actual performance.",
        "component_type": "Payout Timing",
        "keywords": ["Quarterly Payout"]
    }

    # Extract special provisions (Placeholder logic)
    processed_data["special_provisions"].append({
        "description": "Windfall Protection: Medtronic reserves the right to adjust sales credit in case of windfall opportunities.",
        "component_type": "Sales Credit Adjustment",
        "keywords": ["Windfall Protection"]
    })

    # Extract terms & conditions (Placeholder logic)
    processed_data["terms_and_conditions"].append({
        "description": "Eligibility in the plan requires continuous employment and good standing.",
        "component_type": "Employment Requirement",
        "keywords": ["Plan Eligibility", "Continuous Employment"]
    })

    logging.info("✅ Compensation data extracted successfully.")
    return processed_data

if __name__ == "__main__":
    test_text = "Sample compensation plan text with quota bonus and MBO bonus details."
    test_schema = {
        "plan_title": "Test Plan",
        "effective_dates": {"start_date": "2024-01-01", "end_date": "2024-12-31"}
    }
    
    processed_output = analyze_comp_plan(test_text, test_schema)
    with open("test_processed.json", "w") as f:
        json.dump(processed_output, f, indent=4)
    logging.info("✅ Test processed JSON saved.")