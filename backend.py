import flask
from flask_cors import CORS
from flask.json import jsonify
import uuid
from coches import *
import os

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
            coche["id"] = agent.unique_id
            coche["x"] = agent.pos[0]
            coche["y"] = agent.pos[1]
            coche["orient"] = agent.orientation
            coches.append(coche)

        elif type(agent) == Semaforo:
            semaforo = dict()
            semaforo["id"] = agent.unique_id
            semaforo["color"] = agent.light
            semaforo["working"] = agent.working_time
            semaforo["orient"] = agent.orientation
            semaforos.append(semaforo)

        elif type(agent) == Banquetas:
            banqueta = dict()
            banqueta["id"] = agent.unique_id
            banqueta["x"] = agent.pos[0]
            banqueta["y"] = agent.pos[1]
            banuqeta["orient"] = agent.orientation
            banuqetas.append(banqueta)

    dictionary["coches"] = coches
    dictionary["semaforos"] = semaforos
    dictionary["banquetas"] = banquetas

    return jsonify(dictionary)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
