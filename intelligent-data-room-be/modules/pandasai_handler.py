"""PandasAI handler"""

import os
import uuid
import pandas as pd
import pandasai as pai
from pandasai_litellm.litellm import LiteLLM
from .utils import image_to_base64

class PandasAIHandler:
    """Handles data processing and querying using PandasAI."""

    def __init__(self, api_key: str, model_name: str, dataframes: dict[str, pai.DataFrame]):
        self.api_key = api_key
        self.model_name = model_name
        self.llm = LiteLLM(model="gemini/" + model_name, api_key=api_key)
        
        # Global configuration for PandasAI
        pai.config.set({
            "llm": self.llm,
            "save_charts": True,
            "save_charts_path": "exports/charts"
        })
        
        # Reference to stored dataframes
        self.dataframes = dataframes

    def query_dataframe(self, df_id: str, prompt: str):
        """Queries a stored dataframe."""
        if df_id not in self.dataframes:
            return None
        
        df = self.dataframes[df_id]
        response = df.chat(prompt)
        
        chart_base64 = None
        if isinstance(response, str) and response.endswith(".png"):
            chart_base64 = image_to_base64(response)
            
        return response, chart_base64

    def add_dataframe(self, file_content) -> str:
        """Reads a CSV and stores it, returning a unique ID."""
        df_id = str(uuid.uuid4())
        df_raw = pd.read_csv(file_content)
        self.dataframes[df_id] = pai.DataFrame(df_raw)
        return df_id

    def create_and_query(self, data: dict, prompt: str):
        """Creates a temporary dataframe and queries it."""
        df = pai.DataFrame(data)
        response = df.chat(prompt)
        return response

    def get_head(self, df_id: str):
        """Retrieves the header of a stored dataframe."""
        if df_id not in self.dataframes:
            return None
        df = self.dataframes[df_id]

        return df.get_head()