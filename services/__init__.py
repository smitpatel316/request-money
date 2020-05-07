from pymongo import MongoClient

client = MongoClient(host="localhost", port=27017)
db = client.get_database(name="money-request")
