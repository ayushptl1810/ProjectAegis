# ... existing imports ...
from services.input_processor import InputProcessor

# ... existing code ...

input_processor = InputProcessor()

# ... existing code ...

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