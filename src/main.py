import json
import pymongo
from neo4j import GraphDatabase

from flask import Flask


app = Flask(__name__)


from neo4j import GraphDatabase


class Neo4jConnection:

    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
        except Exception as e:
            print("Failed to create the driver:", e)

    def close(self):
        if self.__driver is not None:
            self.__driver.close()

    def query(self, query, parameters=None, db=None):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            session = self.__driver.session(database=db) if db is not None else self.__driver.session()
            response = list(session.run(query, parameters))
        except Exception as e:
            print("Query failed:", e)
        finally:
            if session is not None:
                session.close()
        return response




@app.route('/heartbeat', methods=["GET"])
def get_heartbeat():

    ville_choisie_temporaire = {
        "villeChoisie": "Sherbrooke"
    }

    return json.dumps(ville_choisie_temporaire)


def create_mongodb_database():
    mongo_client= pymongo.MongoClient()
    mongo_databse = mongo_client["restaurants"]
    restos = mongo_databse["restaurants"]

    test_restaurant = {"name": "Benny", "address": "Whatever"}

    x = restos.insert_one(test_restaurant)

    print("MONGODB: {ex}".format(ex=restos.find_one()))


def create_neo4j_database():
    conn = Neo4jConnection(uri="bolt://127.0.0.1:80/",
                           user="neo4j",
                           pwd="difficulties-pushup-gaps")

    print('Neo4j connection ... created ?')
    return conn


if __name__ == '__main__':
    test = create_neo4j_database()
    create_mongodb_database()
    app.run(port=80)