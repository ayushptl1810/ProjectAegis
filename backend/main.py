from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
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

@app.get("/")
async def root():
    return {"message": "Visual Verification Service is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "visual-verification"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=config.SERVICE_PORT)