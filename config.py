import pymongo
import json
from bson import ObjectId

# connection string
# mongo_url = "mongodb+srv://......."

mongo_url = "mongodb://localhost:27017"

client = pymongo.MongoClient(mongo_url)

# get or create the database
db = client.get_database("marchememo3")


class JSONEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, ObjectId):
                return str(obj)

            return json.JSONEncoder.default(obj)


# method to parse/encode ojects into a json string
def json_parse(data):
    return JSONEncoder().encode(data)