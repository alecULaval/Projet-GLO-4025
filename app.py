import json
import random

from decouple import config
from flask import Flask, jsonify, request
import markdown
import markdown.extensions.fenced_code
from geojson import MultiLineString, FeatureCollection, Point
from py2neo import Graph

app = Flask(__name__)


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
    res = base_de_donnee.run(
        "MATCH (r:Restaurant)-[:category_is]->(t:Type) WITH  t,count(r) as types RETURN collect([t.name, types])").evaluate()
    for r in res:
        res_dict[r[0]] = r[1]
    transformed_data = {
        "restaurants": res_dict,
        "longueurCyclable": base_de_donnee.run("MATCH p=()-[r:route]->() RETURN SUM(r.length)").evaluate()
    }

    return jsonify(transformed_data)


@app.route('/readme', methods=["GET"])
def readme():
    readme_file = open("README.md", "r")
    md_template_string = markdown.markdown(
        readme_file.read(), extensions=["fenced_code"]
    )

    return md_template_string


@app.route('/type', methods=["GET"])
def restaurant_type():
    db = get_connection()
    resto_types = db.run("MATCH (n:Type) RETURN collect(n)").evaluate()
    response = []
    for resto_type in resto_types:
        response.append(resto_type["name"])

    return response


@app.route('/starting_point', methods=["GET"])
def starting_point():
    db = get_connection()

    data = request.data
    json_data = json.loads(data)

    if len(json_data["type"]) != 0:
        restaurant_type = json_data["type"][0]
        query_neo4j = \
            f"""
            MATCH (i:Intersection)<-[:is_closest_to]-(res:Restaurant)-[:category_is]->(c:Type)
            WHERE (c.name = "{restaurant_type}") RETURN collect(i) LIMIT 5
            """
        multiple_intersections = db.run(query_neo4j).evaluate()
        # for intersections_index in range(len(multiple_intersections)):
        response = {
            "inter": multiple_intersections
        }

        return jsonify(response)

        # intersection = multiple_intersections[random.randrange(0, len(multiple_intersections) - 1)]
    else:
        intersection = db.run("MATCH (n:Intersection) RETURN n LIMIT 1").evaluate()

    starting_point = Point((intersection["latitude"], intersection["longitude"]))

    response = {
        "starting_point": starting_point
    }

    return jsonify(response)


@app.route('/parcours', methods=['GET'])
def parcours():
    db = get_connection()

    data = request.data
    json_data = json.loads(data)
    path_length = json_data["length"]
    number_of_stops = json_data["numberOfStops"]
    restaurant_types = json_data["type"]
    starting_point = json_data["starting_point"]
    coord_list = starting_point["coordinates"]
    latitude = coord_list[0]
    longitude = coord_list[1]

    intersection_filters = "{latitude: " + str(latitude) + ", longitude: " + str(longitude) + "}"
    max_length = path_length + 100
    min_length = path_length - 100


    #query = f"MATCH (n:Intersection) WHERE n.latitude = {coord_list[0]}"

    neo4j_query = """MATCH p=()-[r:PATH]->() WHERE r.totalCost > {min_length} AND r.totalCost < {max_length}
    UNWIND nodes(p) AS node
    MATCH (i:Intersection {intersection_filters} is_closest_to]-(res:Restaurant)-[:category_is]->(c:Type)
    WHERE (c.name IN {restaurant_types})
    WITH  COLLECT(res) as result, p as paths, count(res) AS num
    WHERE num = {number_of_stops}
    RETURN paths, [re in result | re.name] as resto LIMIT 1""".format(intersection_filters=intersection_filters,
                                                                      restaurant_types=restaurant_types,
                                                                      max_length=max_length,
                                                                      min_length=min_length,
                                                                      number_of_stops=number_of_stops)

    neo4j_response = db.run(neo4j_query).evaluate()

    # response = FeatureCollection()
    response = neo4j_response

    return jsonify(response)


def get_connection():
    # We use split to split the NEO4J_AUTH formatted as "user/password"
    USERNAME = "neo4j"
    PASSWORD = "secret_password_1234"

    base_de_donnee = Graph(INTERNAL_URL, auth=(USERNAME, PASSWORD), secure=False)
    return base_de_donnee


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=80)
