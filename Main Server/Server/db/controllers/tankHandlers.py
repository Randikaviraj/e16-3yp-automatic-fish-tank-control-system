from Server.db.controllers.connection import tank_collection, users_collection


async def addNewTank(tank: dict, email: str):
    try:
        existance=await tank_collection.find_one({"device_id": tank["device_id"]})
        if existance:
            return False
        temp=await tank_collection.insert_one(tank)
        user = await users_collection.find_one({"email": email})
        print(user)
        print(tank["device_id"])
        user["devices"].append(tank["device_id"])
        updated_user = await users_collection.update_one(
            {"email": email}, {"$set": user}
        )
        if updated_user:
            return True
    except:
        print("Error in addNewTank")
        return False
