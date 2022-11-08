import json
from decouple import config
from flask import Flask, jsonify

app = Flask(__name__)

from py2neo import Graph

INTERNAL_URL = config("NEO4J_INTERNAL_URL")

@app.route('/heartbeat', methods=["GET"])
def heartbeat():
    ville_choisie = {
        "villeChoisie": "Cornwall"
    }

    return jsonify(ville_choisie)

@app.route('/extracted_data', methods=["GET"])
def extracted_data():
    base_de_donnee = get_connection()
    restaurant = {
        "nbRestaurants": base_de_donnee.run("MATCH (n:Restaurant) RETURN COUNT(n)").evaluate(),
        "nbSegments": base_de_donnee.run("MATCH p=()-[r:route]->() RETURN COUNT(r)").evaluate()
    }

    return jsonify(restaurant)

@app.route('/transformed_data', methods=["GET"])
def transformed_data():
    base_de_donnee = get_connection()
    res_dict = {}
    res = base_de_donnee.run("MATCH (r:Restaurant)-[:category_is]->(t:Type) WITH  t,count(r) as types RETURN collect([t.name, types])").evaluate()
    for r in res:
        res_dict[r[0]] = r[1]
    transformed_data = {
        "restaurants": res_dict,
        "longueurCyclable": base_de_donnee.run("MATCH p=()-[r:route]->() RETURN SUM(r.length)").evaluate()
    }

    return jsonify(transformed_data)


def get_connection():
    # We use split to split the NEO4J_AUTH formatted as "user/password"
    USERNAME = "neo4j"
    PASSWORD = "secret_password_1234"

    base_de_donnee = Graph(INTERNAL_URL, auth=(USERNAME, PASSWORD), secure=False)
    return base_de_donnee


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8181)
