import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def debug_mongo():
    # Use the URL from .env
    url = 'mongodb+srv://sagar_patel:Vw63HttqKRICjeim@myworkplace.8urqfsf.mongodb.net/'
    client = AsyncIOMotorClient(url)
    db = client['hr_interview']
    
    collections = await db.list_collection_names()
    print(f"Collections in 'hr_interview': {collections}")
    
    for coll_name in collections:
        count = await db[coll_name].count_documents({})
        print(f"Collection: {coll_name}, Count: {count}")
        
        if coll_name == 'video_recording':
            latest = await db[coll_name].find_one(sort=[('created_at', -1)])
            print(f"  Latest in video_recording: {latest}")
            
    client.close()

if __name__ == "__main__":
    asyncio.run(debug_mongo())
