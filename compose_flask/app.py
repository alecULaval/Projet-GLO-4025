import json
from flask import Flask

from compose_flask.mongodb import create_mongodb_database
from compose_flask.neo4jdb import create_neo4j_database

app = Flask(__name__)



@app.route('/heartbeat', methods=["GET"])
def heartbeat():
    ville_choisie = {
        "villeChoisie": "Toronto"
    }

    return json.dumps(ville_choisie)


if __name__ == "__main__":
    test = create_neo4j_database()
    create_mongodb_database()
    app.run(host="0.0.0.0", debug=True, port=80)
