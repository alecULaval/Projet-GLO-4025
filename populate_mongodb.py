import pymongo
import json
from decouple import config

MONGO_CONTAINER_NAME = config("MONGO_CONTAINER_NAME")
USERNAME = config("MONGO_INITDB_ROOT_USERNAME")
PASSWORD = config("MONGO_INITDB_ROOT_PASSWORD")
DB_NAME = config("MONGO_DB_NAME")
RESTAURANT_COLLECTION = config("MONGO_COLLECTION_RESTAURANTS")
INTERSECTION_COLLECTION = config("MONGO_COLLECTION_INTERSECTIONS")

mongo_client = pymongo.MongoClient(f'mongodb://{MONGO_CONTAINER_NAME}', username=USERNAME, password=PASSWORD)
mongo_database = mongo_client[DB_NAME]
restos = mongo_database[RESTAURANT_COLLECTION]
intersections = mongo_database[INTERSECTION_COLLECTION]

with open('resources/restos_cornwall_formatted.json', 'r') as file:
    data = json.load(file)
    for resto in data:
        restaurant = {"_id": resto, "parameters": data[resto]}
        restos.insert_one(restaurant)

with open('resources/intersections.json', 'r') as file:
    data = json.load(file)
    for intersection in data:
        inter = {"_id": intersection, "coordinates": data[intersection]}
        intersections.insert_one(inter)


