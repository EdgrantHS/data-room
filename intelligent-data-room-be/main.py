import os
import pandasai as pai
from pandasai_litellm.litellm import LiteLLM
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from google import genai

# Getting API key from ENV
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Configure PandasAI with LiteLLM
llm = LiteLLM(model="gemini/gemini-2.5-flash-lite", api_key=api_key)
# Global configuration for PandasAI
pai.config.set({"llm": llm})

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