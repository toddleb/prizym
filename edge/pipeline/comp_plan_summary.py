import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def generate_summary(processed_data, insights_data):
    """Aggregate compensation data at Region/BU/Corporate level and generate summary."""
    logging.info("🔹 Generating high-level compensation summary...")

    summary = {
        "plan_title": processed_data.get("plan_title", "Unknown Plan"),
        "region_summary": {},
        "bu_summary": {},
        "corporate_summary": {},
        "key_findings": []
    }

    # Step 1: Group Compensation Data by Region & Business Unit
    for component, details in processed_data.get("compensation_structure", {}).items():
        region = processed_data["plan_summary"]["client_tags"].get("Region", "Unknown Region")
        bu = processed_data["plan_summary"]["client_tags"].get("Business Unit", "Unknown BU")

        if region not in summary["region_summary"]:
            summary["region_summary"][region] = []
        summary["region_summary"][region].append(component)

        if bu not in summary["bu_summary"]:
            summary["bu_summary"][bu] = []
        summary["bu_summary"][bu].append(component)

    # Step 2: Corporate-Level Aggregation
    summary["corporate_summary"]["total_components"] = len(processed_data.get("compensation_structure", {}))
    summary["corporate_summary"]["quota_weighting"] = insights_data["incentive_balance"]["quota_weighting"]
    summary["corporate_summary"]["key_risks"] = insights_data["risk_analysis"]

    # Step 3: High-Level Observations
    summary["key_findings"].extend(insights_data["optimization_recommendations"])

    logging.info("✅ Compensation summary generated successfully.")
    return summary

if __name__ == "__main__":
    with open("test_processed.json", "r") as f:
        processed_data = json.load(f)

    with open("test_insights.json", "r") as f:
        insights_data = json.load(f)

    summary_output = generate_summary(processed_data, insights_data)
    with open("test_summary.json", "w") as f:
        json.dump(summary_output, f, indent=4)

    logging.info("✅ Test summary JSON saved.")