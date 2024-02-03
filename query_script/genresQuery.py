from pymongo import MongoClient
import json

def LCS(s1, s2):
    m = len(s1)
    n = len(s2)
    L = [[0] * (n+1) for i in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if s1[i-1] == s2[j-1]:
                L[i][j] = L[i-1][j-1] + 1
            else:
                L[i][j] = max(L[i-1][j], L[i][j-1])
    return L[m][n]

client = MongoClient('mongodb://localhost:27017/')
db = client['filmlover']


ticket_list = list(db["ticket"].find({}))
film_list = list(db["CrawledFilms"].find({}))
total = 0
for ticket in ticket_list:
    total += ticket["ticket price"]
    for film in film_list:
        if LCS(ticket["film"], film["title"])/min(len(ticket["film"]), len(film["title"])) > 0.7:
            ticket["listed_in"] = film["listed_in"]
            break
    
genre_dict = {}
for ticket in ticket_list:
    for genre in ticket["listed_in"]:
        if genre in genre_dict:
            genre_dict[genre] += ticket["ticket price"]
        else:
            genre_dict[genre] = ticket["ticket price"]


genre_percentage_dict = {}
for genre in genre_dict:
    genre_percentage_dict[genre] = genre_dict[genre]/total*100

genre_dict = list(sorted(genre_dict.items(), key=lambda item: item[1], reverse=True))
genre_percentage_dict = list(sorted(genre_percentage_dict.items(), key=lambda item: item[1], reverse=True))


with open("out_data/genre.json", "w") as f:
    json.dump(genre_dict, f)

with open("out_data/genre_percentage.json", "w") as f:
    json.dump(genre_percentage_dict, f)

print("Danh sách doanh thu theo thể loại:")

for i in range(len(genre_dict)):
    print(genre_dict[i][0],":", genre_dict[i][1],"đ, Chiếm", genre_percentage_dict[i][1], "% tổng doanh thu")