import json

print("Hello World!")


from flask import Flask


app = Flask(__name__)


@app.route('/heartbeat', methods=["GET"])
def get_heartbeat():

    ville_choisie_temporaire = {
        "villeChoisie": "Sherbrooke"
    }

    return json.dumps(ville_choisie_temporaire)


if __name__ == '__main__':
    app.run(port=80)