import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def generate_insights(processed_data):
    """Analyze processed compensation data and generate consulting insights."""
    logging.info("🔹 Generating insights from processed data...")

    insights = {
        "plan_title": processed_data.get("plan_title", "Unknown Plan"),
        "incentive_balance": {},
        "risk_analysis": [],
        "optimization_recommendations": []
    }

    # Step 1: Analyze Incentive Balance
    quota_based = []
    performance_based = []
    
    for component, details in processed_data.get("compensation_structure", {}).items():
        if "Quota" in component:
            quota_based.append(component)
        else:
            performance_based.append(component)

    quota_percentage = len(quota_based) / (len(quota_based) + len(performance_based) or 1) * 100
    insights["incentive_balance"] = {
        "quota_based_components": quota_based,
        "performance_based_components": performance_based,
        "quota_weighting": f"{quota_percentage:.2f}%"
    }

    # Step 2: Identify Potential Risks
    if quota_percentage > 70:
        insights["risk_analysis"].append("⚠️ Over-Reliance on Quotas: More than 70% of incentives are quota-based. Consider balancing with performance-based incentives.")

    if "Recoverable Draw" in processed_data.get("compensation_structure", {}):
        insights["risk_analysis"].append("⚠️ Recoverable Draw Risk: If reps do not meet quota, they may owe back their draw, which could impact retention.")

    if any("Windfall Protection" in sp["description"] for sp in processed_data.get("special_provisions", [])):
        insights["risk_analysis"].append("⚠️ Windfall Protection Clause: Ensure clear guidelines on how windfalls are determined to prevent disputes.")

    # Step 3: Optimization Recommendations
    if quota_percentage > 60:
        insights["optimization_recommendations"].append("✅ Consider shifting 5-10% of compensation from quota-based to performance-based to drive long-term growth.")

    if "Short-Dated Inventory Bonus" in processed_data.get("compensation_structure", {}):
        insights["optimization_recommendations"].append("✅ Short-Dated Inventory Bonus: Ensure clear tracking & reporting to avoid missed payouts due to administrative errors.")

    logging.info("✅ Insights generated successfully.")
    return insights

if __name__ == "__main__":
    with open("test_processed.json", "r") as f:
        processed_data = json.load(f)
    
    insights_output = generate_insights(processed_data)
    with open("test_insights.json", "w") as f:
        json.dump(insights_output, f, indent=4)

    logging.info("✅ Test insights JSON saved.")