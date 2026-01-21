import logging
from fastapi import HTTPException, UploadFile
import pandasai as pai

from modules.env_handler import EnvHandler
from modules.pandasai_handler import PandasAIHandler
from modules.planner import Planner

# Initialize environment
env = EnvHandler()
api_key, model_name = env.get_api_and_model()

# Handlers will be initialized with a reference to main.py's dataframes
pandas_handler = None
planner = None

class APIHandler:
    """Handles the logic of API endpoints"""

    @staticmethod
    def init_handlers(dataframes: dict[str, pai.DataFrame]):
        """Initializes the sub-handlers with a shared dataframe storage."""
        global pandas_handler, planner
        pandas_handler = PandasAIHandler(api_key=api_key, model_name=model_name, dataframes=dataframes)
        planner = Planner(api_key=api_key, model_name=model_name, dataframes=dataframes)

    @staticmethod
    async def test_key():
        """Tests the Gemini API key"""
        try:
            message = planner.generate_content("Say 'Key is working!'")
            return {"status": "success", "message": message}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"API Key Test Failed: {str(e)}")

    @staticmethod
    async def test_pandas():
        """Tests PandasAI with a sample dataframe"""
        try:
            data = {
                "country": ["United States", "United Kingdom", "France", "Germany", "Italy", "Spain", "Canada", "Australia", "Japan", "China"],
                "gdp": [21400000, 2830000, 2710000, 3860000, 2000000, 1390000, 1730000, 1390000, 5080000, 14140000],
                "happiness_index": [6.94, 7.16, 6.66, 7.07, 6.38, 6.40, 7.23, 7.22, 5.87, 5.12]
            }
            prompt = "Which are the 5 happiest countries?"
            response = pandas_handler.create_and_query(data, prompt)
            
            return {
                "status": "success",
                "query": prompt,
                "response": str(response)
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"PandasAI Test Failed: {str(e)}")

    @staticmethod
    async def test_upload_pandas(file: UploadFile):
        """Tests uploading a CSV and querying it"""
        try:
            dataframe_id = pandas_handler.add_dataframe(file.file)
            prompt = "Which are the 5 happiest countries?"
            response, chart_base64 = pandas_handler.query_dataframe(dataframe_id, prompt)
            
            return {
                "status": "success",
                "dataframe_id": dataframe_id,
                "filename": file.filename,
                "query": prompt,
                "response": str(response),
                "chart": chart_base64
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"PandasAI Upload Test Failed: {str(e)}")

    @staticmethod
    async def test_upload_prompt(file: UploadFile, prompt: str):
        """Tests uploading a CSV and querying it with a custom prompt"""
        try:
            dataframe_id = pandas_handler.add_dataframe(file.file)
            response, chart_base64 = pandas_handler.query_dataframe(dataframe_id, prompt)
            
            return {
                "status": "success",
                "dataframe_id": dataframe_id,
                "filename": file.filename,
                "query": prompt,
                "response": str(response),
                "chart": chart_base64
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"PandasAI Upload Prompt Test Failed: {str(e)}")
