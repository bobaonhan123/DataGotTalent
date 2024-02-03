# FilmLover Repository

This repository contains scripts for loading data from Excel files into a MongoDB database.

## Prerequisites

- Python 3.6 or higher
- pandas library
- pymongo library

## Database

We use MongoDB as our database. Make sure MongoDB is installed and running on your local machine on port 27017.

## Data

The data is stored in Excel files. Each file corresponds to a collection in the MongoDB database.

## Scripts

The scripts read data from the Excel files, convert the data into a dictionary format, and then insert the data into the corresponding MongoDB collection.

## How to Run

1. Download and install [mongoDB](https://www.mongodb.com/try/download/community-kubernetes-operator).
2. Download and install [python](https://www.python.org/downloads/release/python-3121/)
3. Clone this:
```bash
git clone https://github.com/bobaonhan123/DataGotTalent.git
```
4. Install the required Python libraries using pip:
```bash
pip install -r requirements.txt
```
5. Run the scripts:
```bash
python script_name.py
```
Replace `script_name.py` with the name of the script you want to run.
