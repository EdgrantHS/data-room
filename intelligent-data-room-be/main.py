from fastapi import FastAPI, UploadFile, File, Form
import pandasai as pai
from modules.api_handler import APIHandler

# Fast API app
app = FastAPI()

# Global storage for dataframes
dataframes: dict[str, pai.DataFrame] = {}
APIHandler.init_handlers(dataframes)

@app.get("/test-gemini")
async def test_key(): return await APIHandler.test_key()

@app.get("/test-pandas")
async def test_pandas(): return await APIHandler.test_pandas()

@app.post("/test-upload-pandas")
async def test_upload_pandas(file: UploadFile = File()): return await APIHandler.test_upload_pandas(file)

@app.post("/test-upload-prompt")
async def test_upload_prompt(file: UploadFile = File(), prompt: str = Form()): return await APIHandler.test_upload_prompt(file, prompt)