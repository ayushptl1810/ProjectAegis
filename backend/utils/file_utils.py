"""
File utility functions
"""

import os
import tempfile
from pathlib import Path
from typing import Optional
from fastapi import UploadFile

async def save_upload_file(file: UploadFile) -> str:
    """
    Save uploaded file to temporary location
    
    Args:
        file: Uploaded file object
        
    Returns:
        Path to saved file
    """
    suffix = Path(file.filename).suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        return tmp.name

def cleanup_temp_files(file_paths: list):
    """
    Clean up temporary files
    
    Args:
        file_paths: List of file paths to delete
    """
    for path in file_paths:
        try:
            if os.path.exists(path):
                os.remove(path)
        except Exception as e:
            print(f"Error cleaning up file {path}: {e}")