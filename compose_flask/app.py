# compose_flask/app.py
import json
from flask import Flask
from redis import Redis

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

"""
@app.route('/')
def hello():
    redis.incr('hits')
    return 'This Compose/Flask demo has been viewed %s time(s).' % redis.get('hits')
"""


@app.route('/heartbeat', methods=["GET"])
def heartbeat():
    ville_choisie_temporaire = {
        "villeChoisie": "Sherbrooke"
    }

    return json.dumps(ville_choisie_temporaire)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
