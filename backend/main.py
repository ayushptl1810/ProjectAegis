from fastapi import FastAPI
import uvicorn
from config import config

app = FastAPI(
    title="Visual Verification Service",
    description="A service to verify images/videos and generate visual counter-measures",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Visual Verification Service is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "visual-verification"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=config.SERVICE_PORT)