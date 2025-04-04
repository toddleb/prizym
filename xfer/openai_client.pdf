#!/usr/bin/env python3
"""
OpenAI integration module with robust error handling and retry logic.
Provides a reusable client for making OpenAI API calls with advanced features.
"""
import os
import time
import random
import logging
import json
from typing import Dict, List, Any, Optional, Union, Tuple, Callable, Type

from functools import wraps
import openai
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Configure logging
logger = logging.getLogger("openai_integration")

def exponential_backoff_retry(max_retries: int = 5, 
                             initial_delay: float = 1, 
                             max_delay: float = 60,
                             jitter: bool = True, 
                             retryable_exceptions: Tuple[Type[Exception], ...] = (openai.OpenAIError, Exception)):
    """
    Decorator for exponential backoff retry logic.
    
    Args:
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay between retries in seconds
        max_delay: Maximum delay between retries in seconds
        jitter: Whether to add randomness to retry delays
        retryable_exceptions: Exception types that should trigger a retry
        
    Returns:
        Decorated function with retry logic
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            delay = initial_delay

            while True:
                try:
                    return func(*args, **kwargs)
                except retryable_exceptions as e:
                    retries += 1
                    
                    # Check if this was a rate limit error from OpenAI
                    rate_limited = False
                    if hasattr(e, 'code') and e.code == 'rate_limit_exceeded':
                        rate_limited = True
                    
                    if retries > max_retries:
                        logger.error(f"Max retries ({max_retries}) exceeded: {str(e)}")
                        raise
                    
                    # Calculate delay with exponential backoff
                    if rate_limited:
                        # Use a longer delay for rate limit errors
                        delay = min(max_delay, delay * 4)
                    else:
                        delay = min(max_delay, delay * 2)
                        
                    # Add jitter if enabled (helps prevent thundering herd problem)
                    if jitter:
                        delay = delay * (0.5 + random.random())
                        
                    logger.warning(f"Attempt {retries}/{max_retries} failed: {str(e)}. "
                                   f"Retrying in {delay:.2f} seconds...")
                    time.sleep(delay)
        return wrapper
    return decorator

class OpenAIProcessor:
    """
    OpenAI API integration with robust error handling and retries.
    Supports multiple models and provides methods for different use cases.
    """
    def __init__(self, 
                api_key: Optional[str] = None, 
                model: str = "gpt-4o", 
                timeout: int = 60, 
                max_retries: int = 5):
        """
        Initialize the OpenAI processor.

        Args:
            api_key: OpenAI API key. If None, uses OPENAI_API_KEY env var.
            model: Model to use for completions.
            timeout: Request timeout in seconds.
            max_retries: Maximum number of retry attempts for API calls.
        """
        # Try to load config first, then fall back to parameters/env vars
        try:
            from config.config import config
            self.api_key = getattr(config, 'OPENAI_API_KEY', None) or api_key or os.environ.get("OPENAI_API_KEY")
            self.model = getattr(config, 'OPENAI_MODEL', None) or model
        except (ImportError, AttributeError):
            # If config import fails, use parameters or environment variables
            self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
            self.model = model
            
        if not self.api_key:
            raise ValueError("OpenAI API key not provided and OPENAI_API_KEY not found in environment")

        self.timeout = timeout
        self.max_retries = max_retries
        
        # Initialize the OpenAI client
        self.client = openai.OpenAI(api_key=self.api_key, timeout=timeout)
        logger.info(f"✅ Initialized OpenAI client with model: {self.model}")
        
    def _handle_api_error(self, e: Exception, context: str) -> None:
        """
        Handle API errors with detailed logging.
        
        Args:
            e: The exception that was raised
            context: Description of the operation that failed
        """
        error_type = type(e).__name__
        error_msg = str(e)
        
        # Log different levels based on error type
        if "InvalidRequestError" in error_type:
            logger.error(f"❌ Invalid request during {context}: {error_msg}")
        elif "RateLimitError" in error_type:
            logger.warning(f"⚠️ Rate limit exceeded during {context}: {error_msg}")
        elif "APIConnectionError" in error_type:
            logger.error(f"❌ API connection error during {context}: {error_msg}")
        elif "APITimeoutError" in error_type:
            logger.error(f"❌ API timeout during {context}: {error_msg}")
        else:
            logger.error(f"❌ Error during {context}: {error_type} - {error_msg}")

    @exponential_backoff_retry(max_retries=5, initial_delay=1)
    def generate_completion(self, 
                           prompt: str, 
                           temperature: float = 0.0, 
                           max_tokens: int = 1500, 
                           system_prompt: Optional[str] = None,
                           stream: bool = False) -> Union[str, Any]:
        """
        Generate a completion using OpenAI with retry logic.

        Args:
            prompt: The prompt to send to OpenAI.
            temperature: Control randomness (0.0 to 1.0).
            max_tokens: Maximum number of tokens to generate.
            system_prompt: Custom system prompt.
            stream: Whether to stream the response.

        Returns:
            The completion text or streaming response.
        """
        try:
            messages = []
            # Add system message if provided
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            else:
                messages.append({"role": "system", "content": "You are a helpful assistant that analyzes compensation plans."})
            # Add user message
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=stream
            )
            
            if stream:
                return response
            else:
                return response.choices[0].message.content
                
        except Exception as e:
            self._handle_api_error(e, "completion generation")
            raise

    @exponential_backoff_retry(max_retries=3, initial_delay=1)
    def generate_json(self, 
                     prompt: str, 
                     schema: Dict[str, Any], 
                     temperature: float = 0.0, 
                     max_tokens: int = 2000) -> Dict[str, Any]:
        """
        Generate structured JSON data using OpenAI.

        Args:
            prompt: The prompt to send to OpenAI.
            schema: JSON schema to validate response against.
            temperature: Control randomness (0.0 to 1.0).
            max_tokens: Maximum number of tokens to generate.

        Returns:
            Parsed JSON data.
        """
        try:
            system_prompt = (
                "You are a helpful assistant that provides structured data. "
                "Your response must be valid JSON according to the schema provided. "
                "Do not include any explanation text, only the JSON data."
            )
            
            # Add schema to the user prompt
            full_prompt = f"Please provide data according to this schema: {json.dumps(schema)}\n\nData to analyze: {prompt}"
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                response_format={"type": "json_object"}
            )
            
            result_text = response.choices[0].message.content
            return json.loads(result_text)
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ Failed to parse JSON response: {str(e)}")
            logger.debug(f"Raw response: {result_text}")
            raise ValueError(f"OpenAI returned invalid JSON: {result_text}")
            
        except Exception as e:
            self._handle_api_error(e, "JSON generation")
            raise

    @exponential_backoff_retry(max_retries=3, initial_delay=1)
    def extract_structured_data(self, 
                               text: str, 
                               extraction_schema: Dict[str, Any], 
                               instructions: str, 
                               examples: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Extract structured data from text using a defined schema and instructions.
        
        Args:
            text: Text to extract data from
            extraction_schema: Schema defining the expected output structure
            instructions: Specific instructions for the extraction task
            examples: Optional few-shot examples to guide the model
            
        Returns:
            Extracted structured data
        """
        try:
            # Build the system prompt
            system_prompt = (
                "You are an AI specialized in extracting structured information from documents. "
                "You will be given text content and must extract the requested information according to the schema."
            )
            
            # Build the user prompt
            user_prompt = f"""
            # Instructions
            {instructions}
            
            # Output Schema
            ```json
            {json.dumps(extraction_schema, indent=2)}
            ```
            
            # Text Content to Analyze
            ```
            {text}
            ```
            """
            
            # Add examples if provided
            if examples and len(examples) > 0:
                examples_text = "# Examples\n"
                for i, example in enumerate(examples):
                    examples_text += f"Example {i+1}:\n```json\n{json.dumps(example, indent=2)}\n```\n\n"
                user_prompt = examples_text + "\n" + user_prompt
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,  # Low temperature for deterministic extraction
                max_tokens=2500,
                response_format={"type": "json_object"}
            )
            
            result_text = response.choices[0].message.content
            return json.loads(result_text)
            
        except Exception as e:
            self._handle_api_error(e, "structured data extraction")
            raise

    @exponential_backoff_retry(max_retries=2, initial_delay=1)
    def estimate_token_count(self, text: str) -> int:
        """
        Estimate the number of tokens in a text string.
        This is a rough estimate based on common tokenization patterns.
        
        Args:
            text: The text to estimate tokens for
            
        Returns:
            Estimated token count
        """
        # Simple estimation: approximate 4 characters per token
        return len(text) // 4

    def get_available_models(self) -> List[str]:
        """
        List available models from OpenAI.
        
        Returns:
            List of available model IDs
        """
        try:
            models = self.client.models.list()
            return [model.id for model in models.data]
        except Exception as e:
            self._handle_api_error(e, "listing models")
            return []

if __name__ == "__main__":
    # Configure logging for testing
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Test the processor
    processor = OpenAIProcessor()
    response = processor.generate_completion("Hello, how are you?")
    print(f"Response: {response}")