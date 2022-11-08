import json
from pymongo import MongoClient, GEOSPHERE
from decouple import config


def initiate_mongodb():
    MONGO_CONTAINER_NAME = config("MONGO_CONTAINER_NAME")
    USERNAME = config("MONGO_INITDB_ROOT_USERNAME")
    PASSWORD = config("MONGO_INITDB_ROOT_PASSWORD")
    DB_NAME = config("MONGO_DB_NAME")
    RESTAURANT_COLLECTION = config("MONGO_COLLECTION_RESTAURANTS")
    INTERSECTION_COLLECTION = config("MONGO_COLLECTION_INTERSECTIONS")
    ROUTE_COLLECTION = config("MONGO_COLLECTION_ROUTES")

    mongo_client = MongoClient(f'mongodb://{MONGO_CONTAINER_NAME}', username=USERNAME, password=PASSWORD)
    mongo_database = mongo_client[DB_NAME]
    restos = mongo_database[RESTAURANT_COLLECTION]
    intersections = mongo_database[INTERSECTION_COLLECTION]
    routes = mongo_database[ROUTE_COLLECTION]

    return restos, intersections, routes


def populate_mongodb():
    restos, intersections, routes = initiate_mongodb()

    with open('resources/restos_cornwall_formatted.json', 'r') as file:
        data = json.load(file)
        for resto in data:
            restaurant = data[resto]
            restaurant = {"_id": resto, "name": restaurant["name"], "types": restaurant["types"],
                          "address": restaurant["address"],
                          "location": create_geojson_point_from_strings(restaurant["longitude"],
                                                                        restaurant["latitude"])}
            restos.insert_one(restaurant)
    restos.create_index([("location", GEOSPHERE)])

    with open('resources/intersections.json', 'r') as file:
        data = json.load(file)
        for intersection in data:
            inter = {"_id": intersection,
                     "location": create_geojson_point_from_strings(data[intersection][0], data[intersection][1])}
            intersections.insert_one(inter)
    intersections.create_index([("location", GEOSPHERE)])

    with open('resources/json_cornwall_reformated.json', 'r') as file:
        data = json.load(file)
        for route in data:
            road = {"_id": route, "length": data[route]["length"], "geometry": data[route]["geometry"]}
            routes.insert_one(road)


def create_geojson_point_from_strings(longitude, latitude):
    return {"type": "Point", "coordinates": [float(longitude), float(latitude)]}
