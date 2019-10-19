from flask_restful import Resource
import requests
import database

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

	def parsePosFields(self, data):
		satelliteFields = {}
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

		year = line1[9:11]
		if (int(year) > 20):
			year = "19" + year
		else:
			year = "20" + year

		return year

# POSITION


	# def getPositionFields()

	def get(self):
		""" Endpoint que faz a requisicão dos dados dos satélites
		"""
		tleFields = self.requestData("https://www.n2yo.com/rest/v1/satellite/tle/39129&apiKey=PWRZDT-4JMAK7-FDEPZM-47V1")
		positionFields = self.requestData("https://www.n2yo.com/rest/v1/satellite/positions/25544/41.702/-76.014/0/2/&apiKey=PWRZDT-4JMAK7-FDEPZM-47V1")
		parsedPosFields = self.parsePosFields(positionFields)
		parseTleFields = self.parseTleFields(tleFields)

		finalDict = {}
		finalDict.update(parseTleFields)
		finalDict.update(parsedPosFields)
		result = database.insertData(finalDict)
		print(finalDict)
		if result:
			ret = True
		else:
			ret = False
		return {'ok': ret}
