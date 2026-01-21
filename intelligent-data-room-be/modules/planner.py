"""Planner handler"""

from google import genai
import pandasai as pai

class Planner:
    """Handles interaction with the Gemini AI model."""

    def __init__(self, api_key: str, model_name: str, dataframes: dict[str, pai.DataFrame]):
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
        self.dataframes = dataframes

    def generate_content(self, prompt: str):
        """Generates content using the Gemini model."""
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text
        except Exception as e:
            raise Exception(f"Gemini API generation failed: {str(e)}")
    
    def generate_plan(self, prompt: str):
        """Generates a plan using the Gemini model based on the prompt and dataframe header."""
        try:
            response = self.client.models.generate_plan(
                model=self.model_name,
                contents="Generate a 5-step plan to answer the following prompt based on the dataframe header, only write the plan steps without any additional text: " + prompt
            )
            return response.plan
        except Exception as e:
            raise Exception(f"Gemini API plan generation failed: {str(e)}")
