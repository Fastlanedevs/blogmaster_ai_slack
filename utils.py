import warnings
warnings.filterwarnings("ignore")
import threading
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from create_blog import create_blog
from dotenv import load_dotenv
load_dotenv()
mongodb_uri = os.getenv("MONGO_DB_URI")
print(mongodb_uri)
 #create a connection to the mongodb
client = MongoClient(mongodb_uri)
db = client["articles"]
collection = db["tasks"]
# mongodb objectId
def create_task(topic):
    id = ObjectId()
    data = collection.insert_one(
        {
            "_id": id,
            "status": "pending",
            "topic": topic,
            "created_at": str(id.generation_time),
        }
    )
    threading.Thread(target=create_blog, args=(id, topic)).start()
    return str(id)

def get_task_status(id):
    data = collection.find_one(
        {
            "_id": ObjectId(id)
        }
    )
    return data["status"]

def get_task_result(id):
    data = collection.find_one(
        {
            "_id": ObjectId(id)
        }
    )
    return data["article"]