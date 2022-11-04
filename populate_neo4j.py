import csv
import json
import time

from Restaurant import Restaurant
from decouple import config
from py2neo import Graph, Node, Relationship
from typing import List


INTERNAL_URL = config("NEO4J_INTERNAL_URL")

# We use split to split the NEO4J_AUTH formatted as "user/password"
USERNAME, PASSWORD = config("NEO4J_CREDENTIALS").split("/")

print('Waiting for servers connections')


# We wait for services Neo4J to start
def validate_neo_connection(url, username, password):
    try:
        print('Trying connection to neo')
        Graph(
            url,
            auth=(username, password),
            secure=False
        )
        print('neo connection works')
    except:
        print('Connection to neo failed, will retry in 10 sec')
        time.sleep(10)
        validate_neo_connection(url=url, username=username, password=password)


def load_csv_to_restaurant() -> List[Restaurant]:
    restaurants_data = []

    with open('resources/restaurant_dataset.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            restaurants_data.append(Restaurant(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
        return restaurants_data


validate_neo_connection(url=INTERNAL_URL, username=USERNAME, password=PASSWORD)
graph = Graph(INTERNAL_URL, auth=(USERNAME, PASSWORD), secure=False)
restaurant_graph = graph.begin()

with open('resources/intersections_only_coords.csv', 'r') as intersection_file:
    reader = csv.reader(intersection_file)
    next(reader)
    for row in reader:
        intersection_node = Node("Intersection", latitude=row[1], longitude=row[0])
        restaurant_graph.create(intersection_node)

with open('resources/routes.json', 'r') as routes_intersections_file, open('resources/json_toronto_reformated.json', 'r') as routes_data_file:
    routes_intersections = json.load(routes_intersections_file)
    routes_data = json.load(routes_data_file)
    for road in routes_intersections:
        road_length = routes_data[road]["length"]
        intersection1_long = routes_intersections[road][0][0]
        intersection1_lat = routes_intersections[road][0][1]
        intersection2_long = routes_intersections[road][1][0]
        intersection2_lat = routes_intersections[road][1][1]
        restaurant_graph.run(f"CREATE (:Intersection {{latitude:{intersection1_lat}, longitude:{intersection1_long}}})"
                             f"-[:Route {{id:{road}, length:{road_length}}}]->"
                             f"(:Intersection {{latitude:{intersection2_lat}, longitude:{intersection2_long}}})")

restaurants = load_csv_to_restaurant()
for restaurant in restaurants:
    restaurant_node = Node("Restaurant", address=restaurant.address, name=restaurant.name, phone=restaurant.phone,
                           price_range=restaurant.price_range, website=restaurant.website, url=restaurant.url,
                           latitude=restaurant.latitude, longitude=restaurant.longitude)
    type_node = Node("Type", name=restaurant.type)
    restaurant_graph.create(restaurant_node)
    restaurant_graph.merge(type_node, primary_label="Type", primary_key="name")
    restaurant_graph.create(Relationship(restaurant_node, "category_is", type_node))


graph.commit(restaurant_graph)
