from pymongo import MongoClient

MONGO_URI = "mongodb+srv://eash210607_db_user:student123@cluster1.4aahrue.mongodb.net/rbac_db?retryWrites=true&w=majority"

client = MongoClient(MONGO_URI)

db = client["rbac_db"]

users_collection = db["users"]
roles_collection = db["roles"]
permissions_collection = db["permissions"]
logs_collection = db["access_logs"]

print("MongoDB Connected ✅")