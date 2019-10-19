from flask_restful import Resource

class SatelliteEndpoints(Resource):
	def get(self):
		""" Endpoint que faz a requisicão dos dados dos satélites
		"""
		return {'hello': 'world'}
