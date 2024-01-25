from pymongo import MongoClient
import json

client = MongoClient('mongodb://localhost:27017/')
db = client['filmlover']

number_of_ticket = db["ticket"].count_documents({})


def ticket_query(slot_type):
    number_of_specific_slot = db["ticket"].count_documents({"slot type": slot_type})
    percentage = number_of_specific_slot / number_of_ticket * 100
    tickets= db["ticket"].find({"slot type": slot_type})
    ticket_list = list(tickets)
    customers = db["customer"].find({})
    customer_list = list(customers)
    for customer in customer_list:
        del customer["_id"]
    for ticket in ticket_list:
        for customer in customer_list:
            if ticket["customerid"] == customer["customerid"]:
                ticket.update(customer)
                break
    male_number = 0
    popcorn_number = 0
    for ticket in ticket_list:
        if ticket["gender"]=="Nam":
            male_number+=1
        if ticket["popcorn"]=="Có":
            popcorn_number+=1
    job_list = db["customer"].distinct("job")
    job_dict = {}
    for job in job_list:
        job_dict[job] = 0
    for ticket in ticket_list:
        job_dict[ticket["job"]]+=1

    job_percentage_dict = {}
    for key in job_dict:
        job_percentage_dict[''.join([key,"_percentage"])] = round(job_dict[key]/len(ticket_list)*100,2)

    result={
        "number_of_specific_slot": number_of_specific_slot,
        "percentage": round(percentage, 2),
        "male_number": male_number,
        "male_percentage": male_number/len(ticket_list)*100,
        "female_number": len(ticket_list)-male_number,
        "female_percentage": (len(ticket_list)-male_number)/len(ticket_list)*100,
        "popcorn_number": popcorn_number,
        "popcorn_percentage": popcorn_number/len(ticket_list)*100,
        "job_list": job_dict,
        "job_percentage_list": job_percentage_dict,
    }
    return result

json.dump(ticket_query("ĐƠN"), open("./out_data/singleTicket.json", "w"))
print(ticket_query("ĐƠN"))

json.dump(ticket_query("ĐÔI"), open("./out_data/doubleTicket.json", "w"))
print(ticket_query("ĐÔI"))
