from fastapi import APIRouter, Depends, Query
import json
import asyncpg

router = APIRouter()


async def get_db():
    return await asyncpg.create_pool(
        user="postgres", password="Fubijar", database="prizym_db", host="localhost"
    )


@router.get("/get-enriched-careers/")
async def get_enriched_careers(
    outlook: str = Query(None, description="Filter by career outlook"),
    title: str = Query(None, description="Filter by career title"),
    limit: int = Query(10, description="Number of results per page"),
    page: int = Query(1, description="Page number (starts from 1)"),
    db=Depends(get_db),
):
    """Fetch enriched careers from `career_cards` with optional filtering & pagination."""
    query = "SELECT * FROM career_cards WHERE 1=1"
    params = []
    filter_clauses = []

    if outlook:
        filter_clauses.append(f"outlook = ${len(params) + 1}")
        params.append(outlook)
    if title:
        filter_clauses.append(f"title::TEXT ILIKE ${len(params) + 1}")
        params.append(f"%{title}%")

    if filter_clauses:
        query += " AND " + " AND ".join(filter_clauses)

    offset = (page - 1) * limit
    query += (
        f" ORDER BY enriched_at DESC LIMIT ${len(params) + 1} OFFSET ${len(params) + 2}"
    )
    params.extend([limit, offset])

    async with db.acquire() as conn:
        careers = await conn.fetch(query, *params)

        parsed_careers = []
        for career in careers:
            parsed_career = dict(career)
            parsed_career["responsibilities"] = json.loads(
                parsed_career["responsibilities"]
            )
            parsed_career["skills"] = json.loads(parsed_career["skills"])
            parsed_career["related_careers"] = json.loads(
                parsed_career["related_careers"]
            )
            parsed_careers.append(parsed_career)

        return parsed_careers
