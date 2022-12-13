import json

from graphdatascience import GraphDataScience
import time
from decouple import config



def validate_neo_connection(url, username, password):
    try:
        print('Trying connection to neo gds')
        GraphDataScience(
            url,
            auth=(username, password),
        )
        print('neo connection works')
    except:
        print('Connection to neo gds failed, will retry in 10 sec')
        time.sleep(10)
        validate_neo_connection(url=url, username=username, password=password)


def initiate_gds():
    INTERNAL_URL = config("NEO4J_INTERNAL_URL")

    # We use split to split the NEO4J_AUTH formatted as "user/password"
    USERNAME, PASSWORD = config("NEO4J_CREDENTIALS").split("/")

    print('Waiting for servers connections for gds')

    validate_neo_connection(url=INTERNAL_URL, username=USERNAME, password=PASSWORD)
    return GraphDataScience(INTERNAL_URL, auth=(USERNAME, PASSWORD))


def create_initial_graph(gds):
    gds.run_cypher(
    """
    CALL gds.graph.project(
        'myGraph',
        'Intersection',
        'route',
        {
            nodeProperties: ['latitude', 'longitude'],
            relationshipProperties: 'length'
        }
    )
    """)


def create_all_possible_path(gds):
    with open('resources/intersections.json', 'r') as intersection_file:
        intersections = json.load(intersection_file)
        for row in intersections:
            s = "{id:'"+row+"'}"
            s2 = '''
            {
                        sourceNode: source,
                        relationshipWeightProperty: 'length',
                        writeRelationshipType: 'PATH',
                        writeNodeIds: true,
                        writeCosts: true
                    })
            '''
            gds.run_cypher(
                f"""
                    MATCH(source:Intersection {s})
                    CALL gds.allShortestPaths.dijkstra.write('myGraph', {s2}
                    YIELD relationshipsWritten
                    RETURN relationshipsWritten
                """
            )



def initiate_graph():
    gds = initiate_gds()
    create_initial_graph(gds)
    create_all_possible_path(gds)

    # gds.graph.project(
    #     'myGraph',
    #     "Intersection",
    #     {
    #         "route": {
    #             "properties": ['latitude', 'longitude'],
    #         } }
    # )
    # print(gds.graph.get("myGraph"))
    # "47a00bff-2d7e-42b4-9fd7-2c167306c778"
    # "95973d86-22d7-48d5-935b-1d925347cedc"
    # MATCH(source:Intersection {id: '47a00bff-2d7e-42b4-9fd7-2c167306c778'}), (target:Intersection {id: '95973d86-22d7-48d5-935b-1d925347cedc'})

