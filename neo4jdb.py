from py2neo import Graph

URL = "bolt://localhost:7687"

# We use split to split the NEO4J_AUTH formatted as "user/password"
USERNAME = "neo4j"
PASSWORD = "secret_password_1234"

base_de_donnee = Graph(URL, auth=(USERNAME, PASSWORD), secure=False)


def create_neo4j_database():
    print("do some")
