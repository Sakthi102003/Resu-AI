from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional

from config import settings


class Database:
    client: Optional[AsyncIOMotorClient] = None
    
    @classmethod
    async def connect_db(cls):
        """Connect to MongoDB"""
        cls.client = AsyncIOMotorClient(settings.MONGODB_URL)
        print(f"✅ Connected to MongoDB: {settings.MONGODB_DB_NAME}")
    
    @classmethod
    async def close_db(cls):
        """Close MongoDB connection"""
        if cls.client:
            cls.client.close()
            print("❌ Closed MongoDB connection")
    
    @classmethod
    def get_db(cls):
        """Get database instance"""
        if cls.client is None:
            raise Exception("Database not connected")
        return cls.client[settings.MONGODB_DB_NAME]


# Helper function to get database
def get_database():
    return Database.get_db()
