import asyncpg
import openai
from typing import Dict, List
import json
import logging
import asyncio
import re
from LENS.ai_models.career_enrichment.chatgpt_service import ChatGPTService

logging.basicConfig(level=logging.INFO)


class CareerEnrichment:
    def __init__(self, db_pool, chatgpt_service):
        self.pool = db_pool
        self.chatgpt = chatgpt_service

    async def get_raw_careers(self) -> List[Dict]:
        """Fetch careers from job_roles that have not been enriched yet."""
        async with self.pool.acquire() as conn:
            careers = await conn.fetch(
                """
                SELECT * FROM job_roles
                WHERE id NOT IN (SELECT job_role_id FROM career_cards)
            """
            )
            if not careers:
                print("🚨 No careers found for enrichment. Check job_roles table.")
            return careers

    async def career_already_enriched(self, career_id: int) -> bool:
        """Check if a career is already enriched in the database."""
        async with self.pool.acquire() as conn:
            result = await conn.fetchval(
                "SELECT COUNT(*) FROM career_cards WHERE job_role_id = $1", career_id
            )
            return result > 0  # ✅ Returns True if career exists, False otherwise

    async def enrich_career(self, career: Dict) -> Dict:
        """Enrich a career using OpenAI."""
        prompt = f"""
        Create a JSON career profile for high school students about {career['title']}:
        {{
            "title": "Career Title",
            "overview": "Brief description",
            "responsibilities": ["Key responsibility 1", "Key responsibility 2"],
            "skills": ["Skill 1", "Skill 2"],
            "education": "Education requirements",
            "salary_range": "Salary range",
            "outlook": "Growing/Stable/Declining",
            "related_careers": ["Related Career 1", "Related Career 2"]
        }}
        """

        print(f"📡 Sending request to OpenAI for: {career['title']}...")

        response = await self.chatgpt.generate_response(prompt, role="career counselor")

        if response:
            try:
                # Remove backticks and any ```json markers
                clean_response = (
                    response.replace("```json", "").replace("```", "").strip()
                )

                # Try parsing the cleaned response
                enriched = json.loads(clean_response)

                # Ensure required keys are present
                required_keys = [
                    "title",
                    "overview",
                    "responsibilities",
                    "skills",
                    "education",
                    "salary_range",
                    "outlook",
                    "related_careers",
                ]
                if not all(key in enriched for key in required_keys):
                    raise ValueError("Missing required keys in the JSON response")

                enriched["job_role_id"] = career["id"]
                print(
                    f"✅ OpenAI Response for {career['title']}: {json.dumps(enriched, indent=2)}"
                )
                return enriched
            except (json.JSONDecodeError, ValueError) as e:
                print(f"🚨 Failed to parse AI response for {career['title']}: {e}")
                print(f"Raw response: {response}")
            return None
        else:
            print(f"🚨 OpenAI returned None for {career['title']}")
        return None

    async def normalize_career_data(self, enriched: Dict) -> Dict:
        """Format enriched career data to fit the database schema, ensuring valid JSON formatting."""

        # Ensure outlook is restricted to ['Growing', 'Stable', 'Declining']
        valid_outlooks = ["Growing", "Stable", "Declining"]
        outlook_text = enriched.get("outlook", "").lower()

        # Assign outlook based on keyword detection
        if "grow" in outlook_text:
            outlook = "Growing"
        elif "stable" in outlook_text:
            outlook = "Stable"
        elif "decline" in outlook_text:
            outlook = "Declining"
        else:
            outlook = "Stable"  # Default to 'Stable' if not clear

        # ✅ Convert fields to proper JSON format
        def safe_json_load(field):
            if isinstance(field, str):
                try:
                    return json.loads(
                        field
                    )  # Convert stringified JSON back to JSON format
                except json.JSONDecodeError:
                    return []
            return field if isinstance(field, list) else []

        return {
            "job_role_id": enriched.get("job_role_id"),
            "title": enriched.get("title", ""),
            "overview": enriched.get("overview", ""),
            "responsibilities": safe_json_load(enriched.get("responsibilities", [])),
            "skills": safe_json_load(enriched.get("skills", [])),
            "education": enriched.get("education", ""),
            "salary_range": str(enriched.get("salary_range", "")),
            "outlook": outlook,  # ✅ Ensuring valid values
            "related_careers": safe_json_load(enriched.get("related_careers", [])),
        }

    async def enrich_all_careers(self):
        """Fetch careers, check if they exist in `career_cards`, enrich using AI only if needed."""
        careers = await self.get_raw_careers()
        if not careers:
            print("🚨 No careers found to enrich.")
            return

    async def upsert_career(self, conn, normalized: Dict):
        """Insert or update an enriched career into career_cards."""
        try:
            await conn.execute(
                """
                INSERT INTO career_cards (job_role_id, title, overview, responsibilities, skills, education,
                                          salary_range, outlook, related_careers, enriched_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, NOW())
                ON CONFLICT (job_role_id) DO UPDATE SET
                    title = EXCLUDED.title,
                    overview = EXCLUDED.overview,
                    responsibilities = EXCLUDED.responsibilities,
                    skills = EXCLUDED.skills,
                    education = EXCLUDED.education,
                    salary_range = EXCLUDED.salary_range,
                    outlook = EXCLUDED.outlook,
                    related_careers = EXCLUDED.related_careers,
                    enriched_at = NOW()
            """,
                normalized["job_role_id"],
                normalized["title"],
                normalized["overview"],
                json.dumps(
                    normalized["responsibilities"]
                ),  # ✅ Convert list to JSON string
                json.dumps(normalized["skills"]),  # ✅ Convert list to JSON string
                normalized["education"],
                normalized["salary_range"],
                normalized["outlook"],
                json.dumps(
                    normalized["related_careers"]
                ),  # ✅ Convert list to JSON string
            )

            print(f"📝 Career {normalized['title']} inserted/updated successfully!")
        except Exception as e:
            print(f"🚨 Failed to insert career {normalized['title']}: {e}")

        async with self.pool.acquire() as conn:
            for career in careers:
                # ✅ Skip AI query if career already exists in `career_cards`
                if await self.career_already_enriched(career["id"]):
                    print(
                        f"✅ Career {career['title']} already enriched. Skipping AI query."
                    )
                    continue

                print(f"🔹 Processing: {career['title']}")  # Debugging
                enriched = await self.enrich_career(career)

                if enriched:
                    normalized = await self.normalize_career_data(enriched)
                    print(
                        f"✅ Enriched: {career['title']} -> Normalized Data: {normalized}"
                    )

                    await self.upsert_career(conn, normalized)
                    print(f"📝 Stored in DB: {career['title']}")


# 🚀 Usage
async def main():
    pool = await asyncpg.create_pool(
        user="postgres", password="Fubijar", database="prizym_db", host="localhost"
    )

    chatgpt_service = ChatGPTService()
    enricher = CareerEnrichment(pool, chatgpt_service)
    await enricher.enrich_all_careers()


if __name__ == "__main__":
    asyncio.run(main())
