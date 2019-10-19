from flask_restful import Resource
import requests
import database
# import logging

class SatelliteEndpoints(Resource):

# TLE

	def requestData(self, url):
		r = requests.get(url=url)
		return r.json()

	def parseTleFields(self, data):
		""" Realiza o parse dos campos retornados pela api
		Arguments:
			fields {dict} -- Campos retornados pela API
		"""

		satelliteFields = {}
		satelliteFields['id'] = data['info']['satid']
		satelliteFields['name'] = data['info']['satname']		
		tle = data['tle']
		satelliteFields['launch_date'] = self.parseTle(tle)
		return satelliteFields


	def parseTle(self, tle):
		""" Realiza a retirada dos campos do tle da requisicão
		
		[description]
		
		Arguments:
			tle {string} -- String do tle
		"""

		line1 = tle[0:70]
		line2 = tle[71:]

		year = line1[9:11]
		if (int(year) > 20):
			year = "19" + year
		else:
			year = "20" + year

		return year

	def get(self):
		""" Endpoint que faz a requisicão dos dados dos satélites
		"""
		tleFields = self.requestData("https://www.n2yo.com/rest/v1/satellite/tle/25544&apiKey=PWRZDT-4JMAK7-FDEPZM-47V1")
		parsedTleFields = self.parseTleFields(tleFields)
		result = database.insertData(parsedTleFields)
		if result:
			ret = 'ok'
		else:
			ret = 'error'
		return {
			'data': ret
		}
		# return {'hello': 'world'}
