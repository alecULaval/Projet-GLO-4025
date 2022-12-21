import json
import random

from decouple import config
from flask import Flask, jsonify, request
import markdown
import markdown.extensions.fenced_code
from geojson import MultiLineString, FeatureCollection, Point, Feature
from py2neo import Graph
from json import encoder

encoder.FLOAT_REPR = lambda o: format(o, '.14f')

app = Flask(__name__)

INTERNAL_URL = config("NEO4J_INTERNAL_URL")


def get_hardcoded_feature_collection():
    features = []
    liste_segments = []
    point_debut_segment1 = (45.02091902673723, -74.70385047566093)
    point_debut_segment2 = (45.03098593467473, -74.70432986437286)
    point_debut_segment3 = (45.02854398654377, -74.71908347589346)
    point_fin_segment1 = (45.12091902673723, -74.80385047566093)
    point_fin_segment2 = (45.12955643743783, -74.80948632768787)
    point_fin_segment3 = (45.12091902673723, -74.81043827634766)
    segment1 = [point_debut_segment1, point_fin_segment1]
    segment2 = [point_debut_segment2, point_fin_segment2]
    segment3 = [point_debut_segment3, point_fin_segment3]
    liste_segments.append(segment1)
    liste_segments.append(segment2)
    liste_segments.append(segment3)

    #Ceci fait a la fin de la boucle sur les nodes des paths
    multiLine_feature = Feature(geometry=MultiLineString(liste_segments))
    multiLine_feature['properties'] = {"length": 12345}

    resto1_feature = Feature(geometry=Point((45.02091902673723, -74.70385047566093)))
    resto2_feature = Feature(geometry=Point((45.02423704238904, -74.71432896432786)))
    resto3_feature = Feature(geometry=Point((45.01947239748320, -74.72079850934897)))
    resto1_feature['properties'] = {"name": "McDonalds", "type": "Burger"}
    resto2_feature['properties'] = {"name": "The Shack", "type": "Pizza"}
    resto3_feature['properties'] = {"name": "Pacini", "type": "Italian"}
    features.append(resto1_feature)
    features.append(resto2_feature)
    features.append(resto3_feature)
    features.append(multiLine_feature)

    response = FeatureCollection(features)
    return response


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

        intersection = multiple_intersections[0]
        random_index_to_select = random.randrange(0, len(multiple_intersections) - 1)
        for i in range(0, len(multiple_intersections)):
            if i == random_index_to_select:
                intersection = multiple_intersections[i]

    else:
        query = "MATCH (n:Intersection) RETURN collect(n) LIMIT 5"
        multiple_intersections = db.run(query).evaluate()

        intersection = multiple_intersections[0]
        random_index_to_select = random.randrange(0, len(multiple_intersections) - 1)
        for i in range(0, len(multiple_intersections)):
            if i == random_index_to_select:
                intersection = multiple_intersections[i]

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
    starting_point = json_data["startingPoint"]
    coord_list = starting_point["coordinates"]
    latitude = coord_list[0]
    longitude = coord_list[1]

    #Temporaire pour le cas avec des types vides
    if len(restaurant_types) ==0:
        restaurant_types = ["Pizza"]

    response = get_hardcoded_feature_collection()

    #intersection_filters = "{" + "latitude:{filter_lat}, longitude: {filter_lon}".format(filter_lat=latitude,
                                                                                   #filter_lon=longitude) + "}"
    #max_length = path_length + 100
    #min_length = path_length - 100

    # query = f"MATCH (n:Intersection) WHERE n.latitude = {coord_list[0]}"
    #neo4j_query = """MATCH p=()-[r:PATH]->() WHERE r.totalCost > {min_length} AND r.totalCost < {max_length}
    #UNWIND nodes(p) AS node
    #MATCH (i:Intersection {intersection_filters})<-[is_closest_to]-(res:Restaurant)-[:category_is]->(c:Type)
    #WHERE (c.name IN {restaurant_types})
    #WITH  COLLECT(res) as result, p as paths, count(res) AS num
    #WHERE num = {number_of_stops}
    #RETURN paths, [re in result | re.name] as resto LIMIT 1""".format(intersection_filters=intersection_filters,
                                                                      #restaurant_types=restaurant_types,
                                                                      #max_length=max_length,
                                                                      #min_length=min_length,
                                                                      #number_of_stops=number_of_stops)

    #neo4j_response = db.run(neo4j_query).evaluate()
    #return jsonify(neo4j_response)

    return jsonify(response)

def get_connection():
    # We use split to split the NEO4J_AUTH formatted as "user/password"
    USERNAME = "neo4j"
    PASSWORD = "secret_password_1234"

    base_de_donnee = Graph(INTERNAL_URL, auth=(USERNAME, PASSWORD), secure=False)
    return base_de_donnee


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=80)
