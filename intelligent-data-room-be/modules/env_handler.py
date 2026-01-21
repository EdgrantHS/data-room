"""Read environment variables"""
import os
from dotenv import load_dotenv

class EnvHandler:
    """Handles environment variable loading and retrieval."""

    def __init__(self, env_file: str = ".env"):
        """Initialize and load environment variables from a file. """
        load_dotenv(dotenv_path=env_file)
        self.api_key = os.environ.get("GEMINI_API_KEY")
        self.model_name = os.environ.get("MODEL_NAME", "gemini-2.5-flash-lite")
    
    def get_api_key(self) -> str:
        """Retrieve the Gemini API key."""
        return self.api_key
    
    def get_model_name(self) -> str:
        """Retrieve the model name."""
        return self.model_name

    def get_api_and_model(self) -> tuple:
        """Retrieve both the API key and model name."""
        return self.api_key, self.model_name