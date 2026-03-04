from motor.motor_asyncio import AsyncIOMotorClient
from config import DATABASE_URI, DATABASE_NAME

mongo = AsyncIOMotorClient(DATABASE_URI)
db = mongo[DATABASE_NAME]

clone_col = db["clones"]

async def add_clone(user_id, token, username):
    await clone_col.insert_one({
        "user_id": user_id,
        "token": token,
        "username": username
    })

async def get_clone(user_id):
    return await clone_col.find_one({"user_id": user_id})

async def get_all_clones():
    clones = []
    async for x in clone_col.find():
        clones.append(x)
    return clones

async def delete_clone(user_id):
    await clone_col.delete_one({"user_id": user_id})
