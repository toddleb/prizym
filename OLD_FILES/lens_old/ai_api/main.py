from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from LENS.ai_api.endpoints import careers

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*",  # Be cautious with this in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(careers.router, prefix="/api")
