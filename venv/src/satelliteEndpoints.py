from flask_restful import Resource
import requests
# import logging

class SatelliteEndpoints(Resource):


	def getFields(self, url):
		r = requests.get(url=url)
		return r



	def parseFields(self, data):
		""" Realiza o parse dos campos retornados pela api
		Arguments:
			fields {dict} -- Campos retornados pela API
		"""

		satelliteFields = {}
		satelliteFields['id'] = data['info']['satid']
		satelliteFields['name'] = data['info']['satname']

		tle = data['tle']
		satelliteFields['tle'] = self.parseTle(tle)
		return satelliteFields


	def parseTle(self, tle):
		""" Realiza a retirada dos campos do tle da requisicão
		
		[description]
		
		Arguments:
			tle {string} -- String do tle
		"""

		tleDict = {}
		line1 = tle[0:70]
		line2 = tle[71:]

		year = line1[9:11]
		if (int(year) > 20):
			year = "19" + year
		else:
			year = "20" + year

		tleDict['year'] = year
		tleDict['inclination'] = line2[8:16]
		tleDict['ascending_node'] = line2[17:25]
		tleDict['eccentricity'] = line2[26:33]
		tleDict['perigee'] = line2[34:42]
		tleDict['revolutions_per_day'] = line2[52:63]
		return tleDict

	def get(self):
		""" Endpoint que faz a requisicão dos dados dos satélites
		"""
		fields = self.getFields("https://www.n2yo.com/rest/v1/satellite/tle/25544&apiKey=PWRZDT-4JMAK7-FDEPZM-47V1")
		data = fields.json()
		parsedFields = self.parseFields(data)
		# print(parsedFields)
		return parsedFields
		# return {'hello': 'world'}
