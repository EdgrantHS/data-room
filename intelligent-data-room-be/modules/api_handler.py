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

dataframe_header = None

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

    @staticmethod
    async def upload_get_head(file: UploadFile):
        """Uploads a CSV and retrieves its head"""
        try:
            global dataframe_header
            dataframe_id = pandas_handler.add_dataframe(file.file)
            header = pandas_handler.get_head(dataframe_id)
        
            dataframe_header = header

            return {
                "status": "success",
                "dataframe_id": dataframe_id,
                "filename": file.filename,
                "header": header
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Upload Get Head Failed: {str(e)}")
    
    @staticmethod
    async def generate_plan_from_prompt(prompt: str):
        """Generates a plan from a given prompt using the Planner"""
        try:
            if dataframe_header is None:
                raise Exception("Dataframe header not set. Please upload a dataframe first.")
            
            plan = planner.generate_plan(prompt, dataframe_header)
            return {
                "status": "success",
                "prompt": prompt,
                "plan": plan
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Generate Plan Failed: {str(e)}")
    
    @staticmethod
    async def execute_plan_on_dataframe(dataframe_id: str, plan: str):
        """Executes a generated plan on a specified dataframe"""
        
        try:
            response = pandas_handler.execute_plan(plan, dataframe_id)
            return {
                "status": "success",
                "dataframe_id": dataframe_id,
                "plan": plan,
                "response": response
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Execute Plan Failed: {str(e)}")