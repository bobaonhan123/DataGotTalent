import pandas as pd
from pymongo import MongoClient
from datetime import datetime
from unidecode import unidecode

client = MongoClient('mongodb://localhost:27017/')
db = client['filmlover']

file_path = 'ticket.xlsx'

data = pd.read_excel(file_path)

data_list = data.to_dict("records")

new_data_list = []

for data in data_list:
    data['film'] = unidecode(str(data['film'])).upper()
    date_time=str(data['date'])[:11]+str(data['time'])
    date_format = '%Y-%m-%d %H:%M:%S'
    date_object = datetime.strptime(date_time, date_format)
    data['date']=date_object
    del data['time']
    check=True
    for key, value in data.items():
        if str(value) == 'nan':
            check=False
    if check:
        new_data_list.append(data)
db['ticket'].insert_many(new_data_list)
