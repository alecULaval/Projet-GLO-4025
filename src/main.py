import json
import pymongo

from flask import Flask


app = Flask(__name__)


@app.route('/heartbeat', methods=["GET"])
def get_heartbeat():

    ville_choisie_temporaire = {
        "villeChoisie": "Sherbrooke"
    }

    return json.dumps(ville_choisie_temporaire)


if __name__ == '__main__':

    mongo_client= pymongo.MongoClient()
    mongo_databse = mongo_client["restaurants"]
    restos = mongo_databse["restaurants"]

    test_restaurant = {"name": "Benny", "address": "Whatever"}

    x = restos.insert_one(test_restaurant)

    print(restos.find_one())

    app.run(port=80)