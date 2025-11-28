"""
Input Processor Service
Processes and routes different types of input to appropriate verifiers
"""

import logging
from typing import Dict, Any, Optional, List
from fastapi import UploadFile

logger = logging.getLogger(__name__)

class InputProcessor:
    """Service for processing various input types"""
    
    def __init__(self):
        """Initialize the input processor"""
        logger.info("InputProcessor initialized")
    
    async def process_input(
        self,
        text_input: Optional[str] = None,
        files: Optional[List[UploadFile]] = None
    ) -> Dict[str, Any]:
        """
        Process input and determine verification type
        
        Args:
            text_input: Text input from user
            files: List of uploaded files
            
        Returns:
            Dictionary with processing results
        """
        try:
            verification_type = "text"
            content = {}
            
            if files and len(files) > 0:
                # Determine if image or video
                file = files[0]
                content_type = file.content_type or ""
                
                if "image" in content_type:
                    verification_type = "image"
                elif "video" in content_type:
                    verification_type = "video"
            
            if text_input:
                content["text"] = text_input
            
            return {
                "verification_type": verification_type,
                "content": content,
                "claim_context": text_input or "Unknown context",
                "claim_date": "Unknown date"
            }
        except Exception as e:
            logger.error(f"Error processing input: {e}")
            return {"error": str(e)}