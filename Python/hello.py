from flask import Flask, render_template, request, jsonify
import json, logging, os, atexit
from http.server import BaseHTTPRequestHandler, HTTPServer

from model import TrafficModel

app = Flask(__name__, static_url_path='')
model = TrafficModel()

def positionsToJSON(ps):
    posDICT = []
    for p in ps:
        pos = {
            "x" : p[0],
            "z" : p[1],
            "y" : p[2]
        }
        posDICT.append(pos)
    return json.dumps(posDICT)

# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8585))

@app.route('/')
def root():
    return jsonify([{"message":"Hello World from IBM Cloud!"}])

@app.route('/multiagentes', methods=['GET', 'POST'])
def multiagntes():
    positions = model.step()
    return positionsToJSON(positions)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
