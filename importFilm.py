import pandas as pd
from pymongo import MongoClient
import os

client = MongoClient('mongodb://localhost:27017/')
db = client['filmlover']

file_path = 'film.xlsx'  

data = pd.read_excel(file_path)

data_dict = data.to_dict("records")

collection_name = os.path.splitext(os.path.basename(file_path))[0]

for data in data_dict:
    splitedData = str(data['listed_in']).split(',')
    finalData = []
    for i in splitedData:
        if i[0] == ' ':
            i = i[1:]
        finalData.append(i)
    data['listed_in'] = finalData
    

db[collection_name].insert_many(data_dict)
