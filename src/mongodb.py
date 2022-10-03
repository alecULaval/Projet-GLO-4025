import pymongo


def create_mongodb_database():
    mongo_client = pymongo.MongoClient()
    mongo_database = mongo_client["restaurants"]
    restos = mongo_database["restaurants"]

    test_restaurant = {"name": "Benny", "address": "Whatever"}

    x = restos.insert_one(test_restaurant)

    print("MONGODB: {ex}".format(ex=restos.find_one()))
