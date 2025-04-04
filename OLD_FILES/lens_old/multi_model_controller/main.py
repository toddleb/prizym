import os
import sys
import time
import openai
import anthropic
import requests
import logging
import logging.handlers
import asyncio
import httpx
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Set
from scripts.keychain_utils import get_secret


# Setup Logging
def setup_logging():
    log_level = os.environ.get("MMC_LOGGING_LEVEL", "INFO").upper()
    log_file = os.environ.get("LOG_FILE_PATH", "./logs/mmc.log")
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.handlers.RotatingFileHandler(
                log_file, maxBytes=10485760, backupCount=5
            ),
            logging.StreamHandler(),
        ],
    )
    return logging.getLogger("MMC")


logger = setup_logging()


# Environment Validation
def validate_environment():
    required_vars = {
        "OPENAI_API_URL": str,
        "CLAUDE_API_URL": str,
        "MIXTRAL_API_URL": str,
        "DEFAULT_AI_MODEL": str,
        "OPENAI_MODEL": str,
        "CLAUDE_MODEL": str,
        "MIXTRAL_MODEL": str,
        "AVAILABLE_MODELS": str,
        "MMC_AI_TIMEOUT": int,
        "MMC_AI_MAX_TOKENS": int,
        "MAX_AI_REQUESTS_PER_MIN": int,
    }

    for var, var_type in required_vars.items():
        value = os.environ.get(var)
        if value is None:
            raise EnvironmentError(f"Missing required environment variable: {var}")
        try:
            if var_type == int:
                int(value)
        except ValueError:
            raise EnvironmentError(
                f"Environment variable {var} must be of type {var_type.__name__}"
            )

    logger.info("Environment validation completed successfully")


# Enhanced Rate Limiter Implementation
class EnhancedRateLimiter:
    def __init__(
        self, requests_per_minute: int, burst_limit: int = None, window_size: int = 60
    ):
        self.requests_per_minute = requests_per_minute
        self.burst_limit = burst_limit or requests_per_minute
        self.window_size = window_size
        self.requests: Dict[str, List[float]] = {}
        self.lock = asyncio.Lock()
        self.blacklist: Set[str] = set()
        self.consecutive_violations: Dict[str, int] = {}

    def _clean_old_requests(self, client_ip: str, now: float):
        if client_ip in self.requests:
            self.requests[client_ip] = [
                req_time
                for req_time in self.requests[client_ip]
                if now - req_time < self.window_size
            ]

    def _is_burst_violation(
        self, client_ip: str, now: float, window: float = 1.0
    ) -> bool:
        recent_requests = len(
            [
                req_time
                for req_time in self.requests.get(client_ip, [])
                if now - req_time < window
            ]
        )
        return recent_requests >= self.burst_limit

    def _update_violation_count(self, client_ip: str):
        self.consecutive_violations[client_ip] = (
            self.consecutive_violations.get(client_ip, 0) + 1
        )
        if self.consecutive_violations[client_ip] >= 5:
            self.blacklist.add(client_ip)
            logger.warning(
                f"IP {client_ip} has been blacklisted due to repeated violations"
            )

    def _clear_violation_count(self, client_ip: str):
        self.consecutive_violations.pop(client_ip, None)

    async def check_rate_limit(self, request: Request) -> bool:
        client_ip = request.client.host
        now = time.time()

        if client_ip in self.blacklist:
            logger.warning(f"Blocked request from blacklisted IP: {client_ip}")
            raise HTTPException(
                status_code=403,
                detail="Your IP has been temporarily blocked due to repeated violations",
            )

        async with self.lock:
            self._clean_old_requests(client_ip, now)

            if client_ip not in self.requests:
                self.requests[client_ip] = []

            if self._is_burst_violation(client_ip, now):
                self._update_violation_count(client_ip)
                logger.warning(f"Burst limit exceeded for IP: {client_ip}")
                raise HTTPException(
                    status_code=429, detail="Too many requests in a short time window"
                )

            request_count = len(self.requests[client_ip])
            if request_count >= self.requests_per_minute:
                self._update_violation_count(client_ip)
                logger.warning(f"Rate limit exceeded for IP: {client_ip}")
                retry_after = self.window_size - (now - min(self.requests[client_ip]))
                raise HTTPException(
                    status_code=429,
                    detail={
                        "error": "Rate limit exceeded",
                        "retry_after": round(retry_after),
                        "limit": self.requests_per_minute,
                        "window": self.window_size,
                        "current_usage": request_count,
                    },
                )

            self.requests[client_ip].append(now)
            self._clear_violation_count(client_ip)
            return True

    async def get_usage(self, client_ip: str) -> dict:
        now = time.time()
        async with self.lock:
            self._clean_old_requests(client_ip, now)
            return {
                "current_requests": len(self.requests.get(client_ip, [])),
                "limit": self.requests_per_minute,
                "remaining": max(
                    0, self.requests_per_minute - len(self.requests.get(client_ip, []))
                ),
                "window_size": self.window_size,
                "is_blacklisted": client_ip in self.blacklist,
                "violations": self.consecutive_violations.get(client_ip, 0),
            }

    async def reset_limits(self, client_ip: str):
        async with self.lock:
            self.requests.pop(client_ip, None)
            self.blacklist.discard(client_ip)
            self.consecutive_violations.pop(client_ip, None)
            logger.info(f"Reset rate limits for IP: {client_ip}")


# Load API Keys
OPENAI_API_KEY = get_secret("OPENAI_API_KEY")
CLAUDE_API_KEY = get_secret("CLAUDE_API_KEY")
MIXTRAL_API_KEY = get_secret("MIXTRAL_API_KEY")

# Load Environment Variables
OPENAI_API_URL = os.environ["OPENAI_API_URL"]
CLAUDE_API_URL = os.environ["CLAUDE_API_URL"]
MIXTRAL_API_URL = os.environ["MIXTRAL_API_URL"]

# API Routes
ROUTE_GPT = os.environ["ROUTE_GPT"]
ROUTE_CLAUDE = os.environ["ROUTE_CLAUDE"]
ROUTE_MIXTRAL = os.environ["ROUTE_MIXTRAL"]
ROUTE_AI = os.environ["ROUTE_AI"]

# AI Model Configuration
DEFAULT_AI_MODEL = os.environ["DEFAULT_AI_MODEL"]
OPENAI_MODEL = os.environ["OPENAI_MODEL"]
CLAUDE_MODEL = os.environ.get("CLAUDE_MODEL", "claude-3-opus-20240229")
MIXTRAL_MODEL = os.environ.get(
    "MIXTRAL_MODEL", "open-mixtral-8x7b"
)  # Updated to open-mixtral-8x7b
AVAILABLE_MODELS = os.environ["AVAILABLE_MODELS"].split(",")

# Processing Settings
MMC_AI_TIMEOUT = int(os.environ["MMC_AI_TIMEOUT"])
MMC_AI_MAX_TOKENS = int(os.environ["MMC_AI_MAX_TOKENS"])
MAX_REQUESTS_PER_MIN = int(os.environ["MAX_AI_REQUESTS_PER_MIN"])

# Initialize FastAPI
app = FastAPI(title="Multi-Model Controller", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Rate Limiter
rate_limiter = EnhancedRateLimiter(
    requests_per_minute=MAX_REQUESTS_PER_MIN,
    burst_limit=int(os.environ.get("MAX_BURST_REQUESTS", 10)),
    window_size=int(os.environ.get("RATE_LIMIT_WINDOW", 60)),
)

# Initialize Claude SDK
claude_client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

# Add base URL to client config if needed
if CLAUDE_API_URL != "https://api.anthropic.com/v1":
    claude_client.base_url = CLAUDE_API_URL


# Add rate limit headers middleware
@app.middleware("http")
async def add_rate_limit_headers(request: Request, call_next):
    response = await call_next(request)
    try:
        usage = await rate_limiter.get_usage(request.client.host)
        response.headers["X-RateLimit-Limit"] = str(usage["limit"])
        response.headers["X-RateLimit-Remaining"] = str(usage["remaining"])
        response.headers["X-RateLimit-Reset"] = str(
            int(time.time() + usage["window_size"])
        )
    except Exception as e:
        logger.error(f"Error adding rate limit headers: {e}")
    return response


# Models
class AIQueryRequest(BaseModel):
    model: Optional[str] = Field(None, description="AI model to use")
    query_key: str = Field(..., min_length=1, max_length=100)
    asks: List[str] = Field(..., min_items=1, max_items=10)
    response_fields: List[str] = Field(default_factory=list)
    refine: Optional[bool] = Field(False)
    fields_to_refine: Optional[List[str]] = Field(default_factory=list)

    @validator("asks")
    def validate_asks(cls, v):
        if any(len(ask) > 4000 for ask in v):
            raise ValueError("Individual asks must not exceed 4000 characters")
        return v

    @validator("model")
    def validate_model(cls, v):
        if v and v not in AVAILABLE_MODELS:
            raise ValueError(f"Invalid model. Must be one of: {AVAILABLE_MODELS}")
        return v


class AIResponse(BaseModel):
    model: str
    response: str
    processing_time: float
    token_count: int


# API Functions
async def query_openai(query: str) -> tuple[str, int]:
    openai_service = OpenAIService()
    return await openai_service.generate_response(query)


class OpenAIService:
    def __init__(self):
        self.openai_key = OPENAI_API_KEY
        if not self.openai_key:
            raise ValueError("No OpenAI API key found")
        self.client = openai.OpenAI(api_key=self.openai_key, base_url=OPENAI_API_URL)

    async def generate_response(self, query: str) -> tuple[str, int]:
        messages = [
            {"role": "system", "content": "You are an AI assistant."},
            {"role": "user", "content": query},
        ]
        try:
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=OPENAI_MODEL,
                messages=messages,
                max_tokens=MMC_AI_MAX_TOKENS,
            )
            return response.choices[0].message.content, response.usage.total_tokens
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))


async def query_claude(query: str) -> tuple[str, int]:
    try:
        logger.info(f"Calling Claude API at: {CLAUDE_API_URL}")
        response = claude_client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=MMC_AI_MAX_TOKENS,
            messages=[{"role": "user", "content": query}],
            system="You are a helpful AI assistant.",  # Added system message
        )

        # Handle Claude's response format
        if hasattr(response, "content") and len(response.content) > 0:
            return response.content[0].text, response.usage.output_tokens
        else:
            logger.error(f"Unexpected Claude response format: {response}")
            raise HTTPException(
                status_code=500, detail="Unexpected response format from Claude"
            )
    except Exception as e:
        logger.error(f"Claude API call failed: {str(e)}")
        logger.error(f"Claude API URL: {CLAUDE_API_URL}")
        logger.error(f"Claude Model: {CLAUDE_MODEL}")
        raise HTTPException(status_code=500, detail=f"Claude API error: {str(e)}")


async def query_mixtral(query: str) -> tuple[str, int]:
    headers = {
        "Authorization": f"Bearer {MIXTRAL_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MIXTRAL_MODEL,
        "messages": [{"role": "user", "content": query}],
        "max_tokens": MMC_AI_MAX_TOKENS,
        "temperature": 0.7,
    }
    try:
        # Use chat/completions endpoint for Mixtral
        api_url = f"{MIXTRAL_API_URL}/chat/completions"
        logger.info(f"Calling Mixtral API at: {api_url}")
        logger.info(f"Payload: {payload}")

        response = requests.post(
            api_url, headers=headers, json=payload, timeout=MMC_AI_TIMEOUT
        )
        response.raise_for_status()
        mistral_response = response.json()

        if "choices" in mistral_response and mistral_response["choices"]:
            return (
                mistral_response["choices"][0]["message"]["content"],
                mistral_response.get("usage", {}).get("total_tokens", 0),
            )
        else:
            logger.error(f"Unexpected Mixtral response format: {mistral_response}")
            raise HTTPException(
                status_code=500, detail="Unexpected response format from Mixtral"
            )
    except requests.exceptions.RequestException as e:
        logger.error(f"Mixtral API connection error: {str(e)}")
        logger.error(
            f"Response content: {e.response.content if hasattr(e, 'response') else 'No response content'}"
        )
        raise HTTPException(status_code=500, detail=f"Mixtral API error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error with Mixtral API: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


# Routes
@app.post(ROUTE_GPT, response_model=AIResponse)
async def query_gpt4(
    request: AIQueryRequest, _: bool = Depends(rate_limiter.check_rate_limit)
):
    start_time = time.time()
    response, token_count = await query_openai(request.asks[0])
    processing_time = time.time() - start_time

    return AIResponse(
        model=OPENAI_MODEL,
        response=response,
        processing_time=processing_time,
        token_count=token_count,
    )


@app.post(ROUTE_CLAUDE, response_model=AIResponse)
async def query_claude_endpoint(
    request: AIQueryRequest, _: bool = Depends(rate_limiter.check_rate_limit)
):
    start_time = time.time()
    response, token_count = await query_claude(request.asks[0])
    processing_time = time.time() - start_time

    return AIResponse(
        model=CLAUDE_MODEL,
        response=response,
        processing_time=processing_time,
        token_count=token_count,
    )


@app.post(ROUTE_MIXTRAL, response_model=AIResponse)
async def query_mixtral_endpoint(
    request: AIQueryRequest, _: bool = Depends(rate_limiter.check_rate_limit)
):
    start_time = time.time()
    response, token_count = await query_mixtral(request.asks[0])
    processing_time = time.time() - start_time

    return AIResponse(
        model=MIXTRAL_MODEL,
        response=response,
        processing_time=processing_time,
        token_count=token_count,
    )


# Rate limit info endpoint
@app.get("/rate-limit-status")
async def rate_limit_status(request: Request):
    return await rate_limiter.get_usage(request.client.host)


# Health Check Endpoint
@app.get("/status")
async def status():
    return {
        "status": "MMC is running",
        "available_models": AVAILABLE_MODELS,
        "default_model": DEFAULT_AI_MODEL,
        "rate_limit": {
            "requests_per_minute": MAX_REQUESTS_PER_MIN,
            "burst_limit": rate_limiter.burst_limit,
            "window_size": rate_limiter.window_size,
        },
    }


# Startup Event
@app.on_event("startup")
async def startup_event():
    validate_environment()
    logger.info("Application startup complete")
