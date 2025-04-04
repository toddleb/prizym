"""
Model Registry: Stores and retrieves AI model configurations.
"""


def get_registered_model(model_name: str):
    """
    Returns the AI model configuration for the given model name.
    """
    model_configs = {
        "default_model": {
            "name": "AI-Model-V1",
            "version": "1.0",
            "parameters": {"temperature": 0.7, "max_length": 512},
        },
        "advanced_model": {
            "name": "AI-Model-V2",
            "version": "2.0",
            "parameters": {"temperature": 0.5, "max_length": 1024},
        },
        "gpt-4": {
            "name": "GPT-4",
            "version": "4.0",
            "parameters": {"temperature": 0.8, "max_length": 2048},
        },
        "claude-3": {
            "name": "Claude-3",
            "version": "3.0",
            "parameters": {"temperature": 0.6, "max_length": 1500},
        },
        "mistral-7b": {
            "name": "Mistral-7B",
            "version": "7.0",
            "parameters": {"temperature": 0.65, "max_length": 1024},
        },
        "gemini-pro": {
            "name": "Gemini-Pro",
            "version": "1.0",
            "parameters": {"temperature": 0.7, "max_length": 1200},
        },
    }

    return model_configs.get(model_name, model_configs["default_model"])


def list_available_models():
    """
    Returns a list of available AI models.
    """
    return list(get_registered_model("").keys())


if __name__ == "__main__":
    # Debugging: Print available models
    print("Available AI Models:", list_available_models())
