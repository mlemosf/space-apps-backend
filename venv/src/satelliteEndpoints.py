from flask_restful import Resource
import requests
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
		satelliteFields['tle'] = self.parseTle(tle)
		return satelliteFields

	def parsePosFields(self, data):
		satelliteFields = {}
		satelliteFields['id'] = data['info']['satid']
		satelliteFields['name'] = data['info']['satname']
		pos = data['positions'][0]
		satelliteFields['pos'] = self.parsePos(pos)
		return satelliteFields
	

	def parsePos(self, pos):
		posDict = {}
		posDict['lat'] = pos['satlatitude']
		posDict['long'] = pos['satlongitude']
		posDict['alt'] = pos['sataltitude']
		return posDict	

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

# POSITION


	# def getPositionFields()

	def get(self):
		""" Endpoint que faz a requisicão dos dados dos satélites
		"""
		# tleFields = self.requestData("https://www.n2yo.com/rest/v1/satellite/tle/39129&apiKey=PWRZDT-4JMAK7-FDEPZM-47V1")
		positionFields = self.requestData("https://www.n2yo.com/rest/v1/satellite/positions/25544/41.702/-76.014/0/2/&apiKey=PWRZDT-4JMAK7-FDEPZM-47V1")
		parsedPosFields = self.parsePosFields(positionFields)

		return parsedPosFields
		# return {'hello': 'world'}
