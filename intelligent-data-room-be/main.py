import os
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from google import genai

# Getting API key from ENV
load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

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