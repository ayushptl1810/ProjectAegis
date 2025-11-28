"""
MongoDB Service for Backend
Handles MongoDB operations for debunk posts
"""

import os
import logging
from typing import List, Dict, Any, Optional
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class MongoDBService:
    """MongoDB service for backend operations"""
    
    def __init__(self, connection_string: Optional[str] = None):
        """Initialize MongoDB connection"""
        self.connection_string = connection_string or os.getenv('MONGO_CONNECTION_STRING')
        
        if not self.connection_string:
            raise ValueError("MongoDB connection string is required")
        
        self.client = None
        self.db = None
        self.collection = None
        
        self._connect()
    
    def _connect(self):
        """Establish MongoDB connection"""
        try:
            self.client = MongoClient(self.connection_string)
            self.client.admin.command('ping')
            self.db = self.client["aegis"]
            self.collection = self.db["debunk_posts"]
            logger.info("✅ MongoDB connected successfully")
        except ConnectionFailure as e:
            logger.error(f"❌ MongoDB connection failed: {e}")
            raise