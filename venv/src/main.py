from flask import Flask
from flask_restful import Resource, Api
from satelliteEndpoints import SatelliteEndpoints

app = Flask(__name__)
api = Api(app)

api.add_resource(SatelliteEndpoints, '/')

if __name__ == '__main__':
	app.run(debug=True)