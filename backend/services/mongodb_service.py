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

# Setup logging
logger = logging.getLogger(__name__)

class MongoDBService:
    """MongoDB service for backend operations"""
    
    def __init__(self, connection_string: Optional[str] = None):
        """Initialize MongoDB connection
        
        Args:
            connection_string: MongoDB connection string. If None, uses MONGO_CONNECTION_STRING env var
        """
        self.connection_string = connection_string or os.getenv('MONGO_CONNECTION_STRING')
        
        if not self.connection_string:
            raise ValueError("MongoDB connection string is required. Set MONGO_CONNECTION_STRING environment variable.")
        
        self.client = None
        self.db = None
        self.collection = None
        
        self._connect()
    
    def _connect(self):
        """Establish MongoDB connection"""
        try:
            self.client = MongoClient(self.connection_string)
            # Test connection
            self.client.admin.command('ping')
            
            # Use 'aegis' database
            self.db = self.client["aegis"]
            self.collection = self.db["debunk_posts"]
            logger.info("✅ MongoDB connected successfully")
        except ConnectionFailure as e:
            logger.error(f"❌ MongoDB connection failed: {e}")
            raise
    
    def get_recent_posts(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get recent debunk posts from MongoDB
        
        Args:
            limit: Maximum number of posts to return
            
        Returns:
            List of recent debunk posts
        """
        try:
            posts = list(
                self.collection.find()
                .sort("created_at", -1)
                .limit(limit)
            )
            
            # Convert ObjectId to string for JSON serialization
            for post in posts:
                if "_id" in post:
                    post["_id"] = str(post["_id"])
            
            logger.info(f"📋 Retrieved {len(posts)} recent debunk posts")
            return posts
            
        except Exception as e:
            logger.error(f"❌ Failed to get recent posts: {e}")
            return []