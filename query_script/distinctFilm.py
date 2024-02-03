from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['filmlover']

li = list(db["ticket"].distinct("film"))

for i in li:
    print(i)