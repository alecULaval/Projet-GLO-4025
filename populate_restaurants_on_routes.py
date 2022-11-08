from py2neo import NodeMatcher, Relationship

from populate_mongodb import initiate_mongodb
from populate_neo4j import initiate_neo4j


def populate_restaurants_on_routes():
    restos, intersections, routes = initiate_mongodb()
    neo4j = initiate_neo4j()
    graph = neo4j.begin()
    nodes = NodeMatcher(graph)
    cursor = restos.find()
    for restaurant in cursor:
        location = restaurant["location"]
        intersection = intersections.find_one({"location": {"$nearSphere": {"$geometry": location}}})
        resto_node = nodes.match("Restaurant", id=restaurant["_id"]).first()
        intersection_node = nodes.match("Intersection", id=intersection["_id"]).first()
        graph.create(Relationship(resto_node, "is_closest_to", intersection_node))

    neo4j.commit(graph)
