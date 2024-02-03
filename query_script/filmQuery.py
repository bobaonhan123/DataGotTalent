from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['filmlover']

totalRevenue = db["ticket"].aggregate([
    {
        "$group": {
            "_id": None,
            "totalRevenue": {
                "$sum": "$ticket price"
            }
        }
    }
])

print("Total revenue:",list(totalRevenue)[0].get("totalRevenue"))
ticket_list = list(db["ticket"].find({}))
film_list = list(db["film"].find({}))

for ticket in ticket_list:
    for film in film_list:
        if ticket["film"] == film["title"]:
            ticket["listed_in"] = film["listed_in"]
            break

print(ticket_list[0])