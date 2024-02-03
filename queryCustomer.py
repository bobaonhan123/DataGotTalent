from pymongo import MongoClient
from datetime import datetime
from dateutil.relativedelta import relativedelta
from collections import defaultdict
from calendar import monthrange
import json
import os

client = MongoClient("mongodb://localhost:27017/")
db = client["filmlover"]
customers = db["customer"].find()




male = db["customer"].count_documents({"gender": "Nam"})
female = db["customer"].count_documents({"gender": "Nữ"})
total = male + female
male_percent = (male / total) * 100
female_percent = (female / total) * 100
print(f"Nam chiếm {male_percent}%, Nữ chiếm {female_percent}%")




now = datetime.now()
age_groups = {"17-27": 0, "28-37": 0, "38-47": 0, "48-59": 0}

for c in customers:
    age = (now - c["DOB"]).days // 365
    if 17 <= age <= 27:
        age_groups["17-27"] += 1
    elif 28 <= age <= 37:
        age_groups["28-37"] += 1
    elif 38 <= age <= 47:
        age_groups["38-47"] += 1
    elif 48 <= age <= 59:
        age_groups["48-59"] += 1

total_count = sum(age_groups.values())
age_percentages = {group: (count / total_count) * 100 for group, count in age_groups.items()}

data = [{"title": group, "percent": percent} for group, percent in age_percentages.items()]

os.makedirs("result", exist_ok=True)
with open("result/age_groups.json", "w") as f:
    json.dump(data, f)

print("Age group percentages have been written to 'result/age_groups.json'.")




jobs = ["student", "teenager", "blue collar", "white collar", "specialist"]
job_counts = {job: db["customer"].count_documents({"job": job}) for job in jobs}

total_count = sum(job_counts.values())
job_percentages = {job: (count / total_count) * 100 for job, count in job_counts.items()}

data = [{"title": job, "percent": percent} for job, percent in job_percentages.items()]

with open("result/job_groups.json", "w") as f:
    json.dump(data, f)

print("Job group percentages have been written to 'result/job_groups.json'.")





tickets = db["ticket"].find()
weekdays = [t["saledate"].weekday() for t in tickets]
weekday_counts = {i: weekdays.count(i) for i in range(7)}

weekday_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
weekday_counts = {weekday_names[i]: count for i, count in weekday_counts.items()}

data = [{"title": day, "count": count} for day, count in weekday_counts.items()]

with open("result/weekday_groups.json", "w") as f:
    json.dump(data, f)

print("Weekday group counts have been written to 'result/weekday_groups.json'.")





tickets = list(db["ticket"].find())
hourly_revenues = defaultdict(int)

for t in tickets:
    hour = t["saledate"].hour
    revenue = t["total"]
    hourly_revenues[str(hour) + "h-" + str(hour+1) + "h"] += revenue

_, num_days = monthrange(tickets[0]["saledate"].year, tickets[0]["saledate"].month)

hourly_avg_revenues = {hour: total_revenue / num_days for hour, total_revenue in hourly_revenues.items()}
print(f"Doanh thu trung bình theo giờ trong ngày: {hourly_avg_revenues}")

sorted_hourly_avg_revenues = sorted(hourly_avg_revenues.items(), key=lambda item: item[1], reverse=True)

with open('result/Time.json', 'w') as f:
    json.dump({hour: {"title": hour, "value": value} for hour, value in sorted_hourly_avg_revenues}, f)
