import flask
from flask_cors import CORS
from flask.json import jsonify
import uuid
from coches import *

games = {}

app = flask.Flask(__name__)
CORS(app)

port = int(os.getenv('PORT', 8000))

@app.route("/")
def root():
    return jsonify([{"message": "Hoooooola! :)"}])

@app.route("/games", methods=["POST"])
def create():
    global games
    id = str(uuid.uuid4())
    games[id] = Calle()

    response = jsonify("ok")
    response.status_code = 201
    response.headers['Location'] = f"/games/{id}"
    response.headers['Access-Control-Expose-Headers'] = '*'
    response.autocorrect_location_header = False
    return response

@app.route("/games/<id>", methods=["GET"])
def queryState(id):
    global model
    model = games[id]
    model.step()
    dictionary = {}
    coches = []
    semaforos = []
    banquetas = []

    for agent in model.schedule.agents:
        if type(agent) == Coche:
            coche = dict()
            coches["id"] = agent.unique_id
            coches["x"] = agent.pos[0]
            coches["y"] = agent.pos[1]
            coches["orient"] = agent.orientation
            coches.append(coche)

        elif type(agent) == Semaforo:
            semaforo = dict()
            semaforos["id"] = agent.unique_id
            semaforos["color"] = agent.light
            semaforos["working"] = agent.working_time
            semaforos["orient"] = agent.orientation
            semaforos.append(semaforo)

        elif type(agent) == Banquetas:
            banqueta = dict()
            banquetas["id"] = agent.unique_id
            banquetas["x"] = agent.pos[0]
            banquetas["y"] = agent.pos[1]
            banuqetas["orient"] = agent.orientation
            banuqetas.append(banqueta)

    dictionary["coches"] = coches
    dictionary["semaforos"] = semaforos
    dictionary["banquetas"] = banquetas

    return jsonify(dictionary)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
