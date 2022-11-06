import json
from flask import Flask

app = Flask(__name__)


@app.route('/heartbeat', methods=["GET"])
def heartbeat():
    ville_choisie = {
        "villeChoisie": "Toronto"
    }

    return json.dumps(ville_choisie)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=80)
