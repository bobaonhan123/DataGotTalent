from pymongo import MongoClient
import json

client = MongoClient('mongodb://localhost:27017/')
db = client['filmlover']

totalRevenueQuery = db["ticket"].aggregate([
    {
        "$group": {
            "_id": None,
            "totalRevenue": {
                "$sum": "$ticket price"
            }
        }
    }
])

totalRevenue = list(totalRevenueQuery)[0].get("totalRevenue")
print("Total revenue:",totalRevenue)

top_films = db["ticket"].aggregate([
    {
        "$group": {
            "_id": "$film",
            "totalRevenue": {
                "$sum": "$ticket price"
            }
        }
    },
    {
        "$sort": {
            "totalRevenue": -1
        }
    },
    {
        "$limit": 5
    }
])

film_list = list(top_films)

for film in film_list:
    film["percentage"] = round(film["totalRevenue"]/totalRevenue*100,2)



with open('./out_data/film_list.json', 'w') as file:
    json.dump(film_list, file)

print("Tổng doanh thu:",totalRevenue)
print("5 phim có doanh thu cao nhất:")
for film in film_list:
    print("- ",film["_id"])
    print("- Doanh thu:",film["totalRevenue"])
    print("- Tỉ lệ:",film["percentage"],"%")
