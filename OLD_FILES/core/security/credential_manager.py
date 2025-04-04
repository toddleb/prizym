import logging
from typing import Optional

import keyring
from huggingface_hub import login

# Configure logging
logging.basicConfig(level=logging.INFO)


class SecureCredentialManager:
    """Secure credential management using macOS Keychain"""

    API_SERVICES = {
        "openai": "OpenAI API",
        "claude": "Anthropic Claude API",
        "mistral": "Mistral AI API",
        "gemini": "Google Gemini API",
        "huggingface": "Hugging Face API",  # Added Hugging Face Key
    }

    DB_SERVICES = {"postgres": "PostgreSQL Database"}

    @staticmethod
    def set_credential(service: str, key_name: str, value: str):
        """Store credentials securely in macOS Keychain"""
        try:
            keyring.set_password(service, key_name, value)
            logging.info(f"✅ Credential stored for {service} ({key_name})")
        except Exception as e:
            logging.error(f"❌ Failed to store credential: {e}")

    @staticmethod
    def get_credential(service: str, key_name: str) -> Optional[str]:
        """Retrieve credentials securely from macOS Keychain"""
        try:
            credential = keyring.get_password(service, key_name)
            if not credential:
                logging.warning(f"⚠ No credential found for {service} ({key_name})")
            return credential
        except Exception as e:
            logging.error(f"❌ Failed to retrieve credential: {e}")
            return None


if __name__ == "__main__":
    print("🔐 Secure Credential Manager for AI Model API Keys & Database Credentials")

    # Store AI Model API Keys without overwriting existing keys
    for service in SecureCredentialManager.API_SERVICES:
        existing_key = SecureCredentialManager.get_credential(service, "api_key")
        if existing_key:
            print(
                f"🔑 Using stored {SecureCredentialManager.API_SERVICES[service]} Key."
            )
        else:
            api_key = input(
                f"Enter {SecureCredentialManager.API_SERVICES[service]} Key (or press Enter to skip): "
            ).strip()
            if api_key:
                SecureCredentialManager.set_credential(service, "api_key", api_key)

    # Store PostgreSQL Database Credentials without overwriting existing ones
    print("\n🔐 Storing PostgreSQL Database Credentials")
    for key in ["db_name", "db_user", "db_password", "db_host", "db_port"]:
        existing_value = SecureCredentialManager.get_credential("postgres", key)
        if existing_value:
            print(f"🔑 Using stored {key.replace('_', ' ').title()}.")
        else:
            value = input(f"Enter PostgreSQL {key.replace('_', ' ').title()}: ").strip()
            if value:
                SecureCredentialManager.set_credential("postgres", key, value)

    print("✅ All Credentials Stored Securely!")

    # Authenticate Hugging Face API
    HF_API_KEY = SecureCredentialManager.get_credential("huggingface", "api_key")
    if HF_API_KEY:
        login(HF_API_KEY)
        print("✅ Hugging Face API authenticated successfully!")
