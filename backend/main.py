# ... existing code ...

from services.video_verifier import VideoVerifier

# ... existing code ...

video_verifier = VideoVerifier()

# ... existing code ...

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