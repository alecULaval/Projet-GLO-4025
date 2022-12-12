from graphdatascience import GraphDataScience
import time
from decouple import config



def validate_neo_connection(url, username, password):
    try:
        print('Trying connection to neo')
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



def initiate_graph():
    gds = initiate_gds()
    gds.graph.project(
        'myGraph',
        "Intersection",
        {
            "route": {
                "properties": ['latitude', 'longitude'],
            } }
    )
    print(gds.graph.get("myGraph"))
    # "47a00bff-2d7e-42b4-9fd7-2c167306c778"
    # "95973d86-22d7-48d5-935b-1d925347cedc"
    # MATCH(source:Intersection {id: '47a00bff-2d7e-42b4-9fd7-2c167306c778'}), (target:Intersection {id: '95973d86-22d7-48d5-935b-1d925347cedc'})

