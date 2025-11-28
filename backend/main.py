from fastapi import FastAPI, File, UploadFile, HTTPException, Form, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn
import os
from typing import Optional

from services.image_verifier import ImageVerifier
from services.text_fact_checker import TextFactChecker
from utils.file_utils import save_upload_file, cleanup_temp_files
from config import config

app = FastAPI(
    title="Visual Verification Service",
    description="A service to verify images/videos and generate visual counter-measures",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize verifiers
image_verifier = ImageVerifier()
text_fact_checker = TextFactChecker()

@app.get("/")
async def root():
    return {"message": "Visual Verification Service is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "visual-verification"}

@app.post("/verify/image")
async def verify_image(
    file: Optional[UploadFile] = File(None),
    image_url: Optional[str] = Form(None),
    claim_context: str = Form("Unknown context"),
    claim_date: str = Form("Unknown date")
):
    """Verify a single image"""
    try:
        temp_file_path = None
        if file is not None:
            temp_file_path = await save_upload_file(file)
        
        result = await image_verifier.verify(
            image_path=temp_file_path,
            claim_context=claim_context,
            claim_date=claim_date,
            image_url=image_url
        )
        
        if temp_file_path:
            cleanup_temp_files([temp_file_path])
        
        return result
    except Exception as e:
        if 'temp_file_path' in locals() and temp_file_path:
            cleanup_temp_files([temp_file_path])
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/verify/text")
async def verify_text(
    text_input: str = Form(...),
    claim_context: str = Form("Unknown context"),
    claim_date: str = Form("Unknown date")
):
    """Verify a textual claim"""
    try:
        result = await text_fact_checker.verify(
            text_input=text_input,
            claim_context=claim_context,
            claim_date=claim_date
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=config.SERVICE_PORT)