from fastapi import FastAPI, File, UploadFile, HTTPException, Form, WebSocket, WebSocketDisconnect
from typing import Optional, List, Dict, Any
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import logging
import json
import asyncio

from services.image_verifier import ImageVerifier
from services.video_verifier import VideoVerifier
from services.input_processor import InputProcessor
from services.text_fact_checker import TextFactChecker
from services.mongodb_service import MongoDBService
from services.websocket_service import connection_manager
from utils.file_utils import save_upload_file, cleanup_temp_files
from config import config

app = FastAPI(
    title="Visual Verification Service",
    description="A service to verify images/videos and generate visual counter-measures",
    version="1.0.0"
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

# Initialize verifiers and input processor
image_verifier = ImageVerifier()
video_verifier = VideoVerifier()
input_processor = InputProcessor()
text_fact_checker = TextFactChecker()

# Initialize MongoDB service
mongodb_service = None
try:
    mongodb_service = MongoDBService()
except Exception as e:
    print(f"Warning: MongoDB service initialization failed: {e}")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await connection_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await connection_manager.send_personal_message(
                json.dumps({"type": "pong", "message": "Connection active"}),
                websocket
            )
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)

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

@app.post("/verify/video")
async def verify_video(
    file: Optional[UploadFile] = File(None),
    video_url: Optional[str] = Form(None),
    claim_context: str = Form("Unknown context"),
    claim_date: str = Form("Unknown date")
):
    """Verify a video"""
    try:
        temp_file_path = None
        if file is not None:
            temp_file_path = await save_upload_file(file)
        
        result = await video_verifier.verify(
            video_path=temp_file_path,
            claim_context=claim_context,
            claim_date=claim_date,
            video_url=video_url
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

@app.post("/chatbot/verify")
async def chatbot_verify(
    text_input: Optional[str] = Form(None),
    files: Optional[List[UploadFile]] = File(None)
):
    """Chatbot-friendly endpoint for verification"""
    try:
        processed_input = await input_processor.process_input(
            text_input=text_input,
            files=files
        )
        
        if "error" in processed_input:
            return {"error": processed_input["error"]}
        
        verification_type = processed_input["verification_type"]
        content = processed_input["content"]
        
        results = []
        
        if verification_type == "text" and content.get("text"):
            result = await text_fact_checker.verify(
                text_input=content["text"],
                claim_context=processed_input["claim_context"],
                claim_date=processed_input["claim_date"]
            )
            results.append(result)
        
        return {
            "message": "Verification completed",
            "verdict": "uncertain",
            "details": {
                "results": results,
                "verification_type": verification_type
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/mongodb/recent-posts")
async def get_recent_debunk_posts(limit: int = 5):
    """
    Get recent debunk posts from MongoDB
    
    Args:
        limit: Maximum number of posts to return (default: 5)
        
    Returns:
        List of recent debunk posts
    """
    try:
        if not mongodb_service:
            raise HTTPException(
                status_code=503,
                detail="MongoDB service is not available. Check MONGO_CONNECTION_STRING environment variable."
            )
        
        posts = mongodb_service.get_recent_posts(limit)
        return {
            "success": True,
            "count": len(posts),
            "posts": posts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=config.SERVICE_PORT)