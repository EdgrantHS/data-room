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
            return None, None
        
        df = self.dataframes[df_id]
        response = df.chat(prompt)
        
        chart_base64 = None
        response_str = str(response)
        
        # Check if it's a ChartResponse or ends with .png
        is_chart = (hasattr(response, '__class__') and 'ChartResponse' in response.__class__.__name__) or \
                   (isinstance(response_str, str) and response_str.endswith(".png"))
        
        if is_chart:
            chart_base64 = image_to_base64(response_str)
            
        return response_str, chart_base64

    def add_dataframe(self, file_content) -> str:
        """Reads a CSV and stores it, returning a unique ID."""
        df_id = str(uuid.uuid4())
        df_raw = pd.read_csv(file_content)
        self.dataframes[df_id] = pai.DataFrame(df_raw)
        return df_id

    def get_head(self, df_id: str) -> str:
        """Returns the first few rows of the dataframe as a string."""
        if df_id in self.dataframes:
            return self.dataframes[df_id].head().to_string()
        return "Dataframe not found."

    def create_and_query(self, data: dict, prompt: str) -> str:
        """Creates a temporary dataframe and queries it."""
        df = pai.DataFrame(data)
        response = df.chat(prompt)
        return response
    
    def execute_plan(self, plan: str, df_id: str) -> str:
        """Executes a plan of actions on the specified dataframe.
        If an image is generated, returns its base64 representation.
        """
        if df_id not in self.dataframes:
            return "Dataframe not found."
        
        df = self.dataframes[df_id]
        response = df.chat(plan)
        
        # Check if response is a ChartResponse object, the type that PandasAI uses for charts
        response_str = str(response)
        if hasattr(response, '__class__') and 'ChartResponse' in response.__class__.__name__:
            image_path = response_str
            base64_result = image_to_base64(image_path)
            return base64_result if base64_result else image_path
        
        # Also check if string response ends with .png
        if isinstance(response_str, str) and response_str.endswith(".png"):
            base64_result = image_to_base64(response_str)
            return base64_result if base64_result else response_str
        
        return response_str
        
