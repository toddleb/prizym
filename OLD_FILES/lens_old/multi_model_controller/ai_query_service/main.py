import openai
import os
import sys
import os

sys.path.append(os.path.expanduser("~/Prizym/scripts"))  # Ensure SCRIPTS is importable
from keychain_utils import get_secret

import psycopg2
import json
import hashlib
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Load environment variables
env_path = os.path.expanduser("~/Prizym/.env")
load_dotenv(env_path)

# Retrieve API key, database credentials, and OpenAI model
OPENAI_API_KEY = get_secret("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo")  # Default to GPT-4 Turbo
DB_HOST = os.getenv("DB_HOST", "host.docker.internal")  # Ensure Docker compatibility
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = get_secret("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME", "prizym_db")

# Initialize FastAPI
app = FastAPI()


# Define API request schema
class GPTQueryRequest(BaseModel):
    gpt_name: str
    query_key: str
    asks: List[str]
    response_fields: List[str]
    refine: Optional[bool] = False
    fields_to_refine: Optional[List[str]] = []


# ✅ STUBBED FUNCTION FOR NOW - We will replace this later
def process_ai_query(query):
    """
    Placeholder function for AI query processing.
    This will be replaced with a full implementation later.
    """
    return f"Stubbed AI response for query: {query}"


# ✅ AI-powered career guidance class (for later use)
class NextNavigatorGPT:
    """
    AI-powered career guidance system for Prizym Navigator.
    This class handles:
    - Checking the database for cached responses.
    - Sending user career questions to OpenAI's GPT model.
    - Logging questions & AI responses into the PostgreSQL database.
    """

    def __init__(self):
        """Initialize the OpenAI client using the API key and model."""
        self.api_key = OPENAI_API_KEY
        self.model = OPENAI_MODEL
        self.client = openai.OpenAI()

    def get_career_guidance(self, user_question: str) -> str:
        """Checks the database for an existing answer before querying OpenAI."""
        cached_response = self.check_cached_response(user_question)
        if cached_response:
            return cached_response

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are NEXT Navigator, an AI-powered career advisor.",
                    },
                    {"role": "user", "content": user_question},
                ],
                store=True,
            )
            guidance = response.choices[0].message.content
            self.save_to_database(user_question, guidance)
            return guidance
        except Exception as e:
            return f"Error fetching response: {str(e)}"

    def check_cached_response(self, question: str):
        """Checks if the response already exists in the database."""
        try:
            with psycopg2.connect(
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port="5432",
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT response_text FROM query_responses 
                        JOIN query_requests ON query_responses.request_id = query_requests.id 
                        WHERE query_requests.query_text = %s LIMIT 1;
                        """,
                        (question,),
                    )
                    result = cursor.fetchone()
                    return result[0] if result else None
        except psycopg2.Error as err:
            print(f"❌ PostgreSQL Error: {err}")
        except Exception as e:
            print(f"❌ General Error: {str(e)}")
        return None

    def save_to_database(self, question: str, response: str):
        """Saves AI queries and responses into the PostgreSQL `query_requests` table."""
        try:
            with psycopg2.connect(
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port="5432",
            ) as connection:
                with connection.cursor() as cursor:
                    insert_query = "INSERT INTO query_requests (user_id, query_text) VALUES (%s, %s) RETURNING id;"
                    cursor.execute(insert_query, (1, question))
                    request_id = cursor.fetchone()[0]
                    insert_response_query = """
                    INSERT INTO query_responses (request_id, gpt_model_id, response_text, response_metadata)
                    VALUES (%s, %s, %s, %s);
                    """
                    cursor.execute(
                        insert_response_query,
                        (request_id, 1, response, '{"source": "GPT-4o"}'),
                    )
                    connection.commit()
        except psycopg2.Error as err:
            print(f"❌ PostgreSQL Error: {err}")
        except Exception as e:
            print(f"❌ General Error: {str(e)}")


# ✅ FastAPI Endpoint - Queries GPT (Will use NextNavigatorGPT later)
@app.post("/query-gpt")
def query_gpt(request: GPTQueryRequest):
    try:
        return {
            "gpt_name": request.gpt_name,
            "response": process_ai_query(request.asks[0]),
            "cached": False,
        }
    except Exception as e:
        return {"error": str(e)}


# ✅ FastAPI Endpoint - Database Connection Test


@app.get("/db-test")
def db_test():
    try:
        db_name = os.getenv("DB_NAME")
        db_user = os.getenv("DB_USER")
        db_host = os.getenv("DB_HOST", "host.docker.internal")
        db_port = os.getenv("DB_PORT", "5432")
        db_password = get_secret("DB_PASSWORD")  # Retrieve password before connection

        print(
            f"🔍 Connecting to DB: {db_name}, User: {db_user}, Host: {db_host}, Port: {db_port}"
        )

        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users;")
        result = cursor.fetchone()
        conn.close()
        return {"message": "Database connection successful!", "user_count": result[0]}
    except Exception as e:
        print(f"❌ Database Connection Error: {e}")
        return {"error": str(e)}
