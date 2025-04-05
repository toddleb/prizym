#!/usr/bin/env python3
"""
Database Schema Loader
- Fetches full database schema (tables, columns, and types).
- Stores schema in memory and logs it for future reference.
"""

import psycopg2
import json
from config.config import config

def get_database_schema():
    """Fetches and returns the database schema as a dictionary."""
    schema = {}

    try:
        conn = psycopg2.connect(
            dbname=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            host=config.DB_HOST,
            port=config.DB_PORT
        )
        cur = conn.cursor()

        # Fetch table names and columns
        cur.execute("""
            SELECT table_name, column_name, data_type
            FROM information_schema.columns
            WHERE table_schema = 'public'
            ORDER BY table_name, ordinal_position;
        """)
        rows = cur.fetchall()

        for table, column, data_type in rows:
            if table not in schema:
                schema[table] = {}
            schema[table][column] = data_type

        cur.close()
        conn.close()
        return schema

    except Exception as e:
        print(f"❌ Error fetching schema: {e}")
        return {}

# Load schema into memory
db_schema = get_database_schema()

# Save schema to a JSON file for logging
schema_file = "database_schema.json"
with open(schema_file, "w") as f:
    json.dump(db_schema, f, indent=2)

print(f"✅ Database schema saved to {schema_file}")