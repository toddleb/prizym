#!/usr/bin/env python3
"""
Master Batch Processing Pipeline
- Runs batch processing
- Monitors status
- Retrieves and processes results
"""

import argparse
import logging
import time
import openai
from src.pipeline.document_processor_batch import BatchDocumentProcessor, process_large_batches

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("batch_pipeline")

def monitor_and_retrieve(batch_id):
    """Continuously monitors batch status and retrieves results when complete."""
    processor_instance = BatchDocumentProcessor()

    logger.info(f"📡 Monitoring batch: {batch_id}")
    
    while True:
        status = processor_instance.check_batch_status(batch_id)
        if status == "completed":
            logger.info(f"✅ Batch {batch_id} completed! Retrieving results...")
            processor_instance.retrieve_results(batch_id)
            break
        elif status in ["failed", "cancelled"]:
            logger.error(f"❌ Batch {batch_id} failed or was cancelled.")
            break
        else:
            logger.info(f"⏳ Batch {batch_id} still in progress... Checking again in 60s.")
            time.sleep(60)

def main():
    """CLI interface for batch processing pipeline."""
    parser = argparse.ArgumentParser(description="Batch Processing Pipeline Super Script")
    parser.add_argument("--limit", "-l", type=int, default=10000, help="Max documents to process")
    parser.add_argument("--monitor", "-m", type=str, help="Monitor batch status and retrieve results")
    
    args = parser.parse_args()

    if args.monitor:
        monitor_and_retrieve(args.monitor)
    else:
        process_large_batches(limit=args.limit)

if __name__ == "__main__":
    main()