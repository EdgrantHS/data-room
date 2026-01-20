import os
import base64
from dotenv import load_dotenv

import uuid
import pandas as pd
import pandasai as pai
from pandasai_litellm.litellm import LiteLLM

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from google import genai

# Getting API key from env
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Global sessions storage, for storing dataframes
dataframes = {}

llm = LiteLLM(model="gemini/gemini-2.5-flash-lite", api_key=api_key)
# Global configuration for PandasAI
pai.config.set({
    "llm": llm,
    "save_charts": True,
    "save_charts_path": "exports/charts"
})

def image_to_base64(image_path: str) -> str:
    """Converts an image file to a base64 string."""
    try:
        if os.path.exists(image_path):
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Error converting image to base64: {e}")
    return None

# Fast API app
app = FastAPI()

@app.get("/test-gemini")
async def test_key():
    try:
        response = client.models.generate_content(
            # Using gemini 2.5 flash lite model
            model="gemini-2.5-flash-lite", 
            contents="Say 'Key is working!'"
        )
        return {"status": "success", "message": response.text}
    except Exception as e:
        # This will catch invalid keys, rate limits, or network issues
        raise HTTPException(status_code=500, detail=f"API Key Test Failed: {str(e)}")

@app.get("/test-pandas")
async def test_pandas():
    try:
        # Hard coded sample dataframe
        data = {
            "country": ["United States", "United Kingdom", "France", "Germany", "Italy", "Spain", "Canada", "Australia", "Japan", "China"],
            "gdp": [21400000, 2830000, 2710000, 3860000, 2000000, 1390000, 1730000, 1390000, 5080000, 14140000],
            "happiness_index": [6.94, 7.16, 6.66, 7.07, 6.38, 6.40, 7.23, 7.22, 5.87, 5.12]
        }
        df = pai.DataFrame(data)
        
        # Test query
        prompt = "Which are the 5 happiest countries?"
        
        response = df.chat(prompt)
        
        return {
            "status": "success",
            "query": prompt,
            "response": str(response)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PandasAI Test Failed: {str(e)}")

@app.post("/test-upload-pandas")
async def test_upload_pandas(file: UploadFile = File()):
    try:
        # Generate a unique dataframe ID
        dataframe_id = str(uuid.uuid4())
        
        # Read file
        df_raw = pd.read_csv(file.file)
        
        # Store the dataframe with the generated ID
        dataframes[dataframe_id] = pai.DataFrame(df_raw)
        
        # Test query
        df = dataframes[dataframe_id]
        prompt = "Which are the 5 happiest countries?"
        response = df.chat(prompt)
        
        # Check if response is a chart path
        chart_base64 = None
        if isinstance(response, str) and response.endswith(".png"):
            chart_base64 = image_to_base64(response)
        
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


@app.post("/test-upload-prompt")
async def test_upload_prompt(file: UploadFile = File(), prompt: str = Form()):
    try:
        # Generate a unique dataframe ID
        dataframe_id = str(uuid.uuid4())
        
        # Read file
        df_raw = pd.read_csv(file.file)
        
        # Store the dataframe with the generated ID
        dataframes[dataframe_id] = pai.DataFrame(df_raw)
        
        # Query using the prompt provided in the request body
        df = dataframes[dataframe_id]
        response = df.chat(prompt)
        
        # Check if response is a chart path
        chart_base64 = None
        if isinstance(response, str) and response.endswith(".png"):
            chart_base64 = image_to_base64(response)
        
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

