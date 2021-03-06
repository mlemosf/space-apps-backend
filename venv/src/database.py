from pymongo import MongoClient

client = MongoClient()
db = client.pymongo_test

def insertData(data):
	try:
		satellite = db.satellite
		result = satellite.insert_one(data)
		print('One post: {0}'.format(result.inserted_id))
		ret = True
	except Exception:
		print("Couldn't store data on database")
		ret = False
	return ret

def getData():
	try:
		satellite = db.satellite
		result = satellite.find({}, {'_id': False})
	except Exception:
		print("Couldn't find data on database")
	return result
