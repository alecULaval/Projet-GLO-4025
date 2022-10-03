import json

from flask import Flask

from src.mongodb import create_mongodb_database
from src.neo4jdb import create_neo4j_database

app = Flask(__name__)


@app.route('/heartbeat', methods=["GET"])
def get_heartbeat():

    ville_choisie_temporaire = {
        "villeChoisie": "Sherbrooke"
    }

    return json.dumps(ville_choisie_temporaire)


if __name__ == '__main__':
    test = create_neo4j_database()
    create_mongodb_database()
    app.run(port=80)
