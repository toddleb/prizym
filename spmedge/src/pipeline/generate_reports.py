#!/usr/bin/env python3
"""
Generate Reports - Summarizes AI-extracted compensation data from documents.
- Aggregates compensation components, payout structures, and special provisions.
- Outputs structured reports in Markdown, CSV, and JSON formats.
"""

import os
import json
import logging
import pandas as pd
from pathlib import Path
from config.config import config
from src.pipeline.db_integration import DBManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("generate_reports")

# Initialize DB Manager
db_manager = DBManager()

def fetch_extracted_data():
    """Fetch AI-processed compensation data from the database."""
    try:
        db_manager.cursor.execute("SELECT id, name, metadata FROM documents ORDER BY updated_at DESC LIMIT 10;")
        results = db_manager.cursor.fetchall()
        return results
    except Exception as e:
        logger.error(f"❌ Failed to fetch extracted data: {e}")
        return []

def generate_summary_table(data):
    """Generate a summary DataFrame from extracted compensation data."""
    records = []
    for doc_id, name, metadata in data:
        meta = metadata if isinstance(metadata, dict) else json.loads(metadata)
        for component in meta.get("compensation_components", []):
            records.append({
                "Document Name": name,
                "Plan Title": meta.get("plan_title", "Unknown"),
                "Component Name": component.get("name", "N/A"),
                "Type": component.get("type", "N/A"),
                "Frequency": component.get("frequency", "N/A"),
                "Target Amount": component.get("target_amount", "N/A")
            })
    return pd.DataFrame(records)

def save_reports(df):
    """Save reports in different formats."""
    output_dir = Path(config.REPORTS_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save CSV
    csv_path = output_dir / "compensation_summary.csv"
    df.to_csv(csv_path, index=False)
    logger.info(f"✅ CSV Report saved: {csv_path}")
    
    # Save JSON
    json_path = output_dir / "compensation_summary.json"
    df.to_json(json_path, orient="records", indent=2)
    logger.info(f"✅ JSON Report saved: {json_path}")
    
    # Save Markdown
    md_path = output_dir / "compensation_summary.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(df.to_markdown(index=False))
    logger.info(f"✅ Markdown Report saved: {md_path}")

def main():
    """Main report generation function."""
    logger.info("📊 Generating Compensation Reports...")
    extracted_data = fetch_extracted_data()
    if not extracted_data:
        logger.warning("⚠ No extracted compensation data found.")
        return
    
    summary_df = generate_summary_table(extracted_data)
    save_reports(summary_df)
    logger.info("🎯 Report Generation Complete.")

if __name__ == "__main__":
    main()