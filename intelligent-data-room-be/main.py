from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import pandasai as pai
from modules.api_handler import APIHandler

# Fast API app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global storage for dataframes
dataframes: dict[str, pai.DataFrame] = {}
APIHandler.init_handlers(dataframes)

@app.get("/test-gemini")
async def test_key(): return await APIHandler.test_key()

@app.get("/test-pandas")
async def test_pandas(): return await APIHandler.test_pandas()

@app.post("/test-upload-pandas")
async def test_upload_pandas(file: UploadFile = File()): 
    return await APIHandler.test_upload_pandas(file)

@app.post("/test-upload-prompt")
async def test_upload_prompt(file: UploadFile = File(), prompt: str = Form()): 
    return await APIHandler.test_upload_prompt(file, prompt)

@app.post("/upload")
async def upload(file: UploadFile = File()):
    return await APIHandler.upload(file)

@app.post("/generate-plan")
async def generate_plan(dataframe_id: str = Form(), prompt: str = Form()):
    return await APIHandler.generate_plan_from_prompt(dataframe_id, prompt)

@app.post("/execute-plan")
async def execute_plan(dataframe_id: str = Form(), plan: str = Form()):
    return await APIHandler.execute_plan_on_dataframe(dataframe_id, plan)