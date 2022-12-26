from pymongo import MongoClient
from datetime import datetime

client = MongoClient('mongodb://localhost:27017/')
result1 = client['testDB']['penna'].aggregate([
    {
        '$group': {
            '_id': '$Timestamp', 
            'totalvotes': {
                '$sum': '$totalvotes'
            }
        }
    }
])

result = []

for t1 in result1:
    result.append({"_id": datetime.strptime(t1["_id"], "%Y-%m-%d %H:%M:%S"), "totalvotes": t1["totalvotes"]})

output = []

for curr in result:
    prev = max((date for t3 in result if (date := t3["_id"]) < curr["_id"]), default = "")
    if prev == "":
        output.append({'_id': curr["_id"], 'totalvotes': curr["totalvotes"]})
        continue
    for t2 in result:
        if t2["_id"] == prev:
            output.append({'_id': curr["_id"], 'totalvotes': curr["totalvotes"] - t2["totalvotes"]})
            break

final_result = []

maximum_total_vote_increment = max(i["totalvotes"] for i in output)

for cursor in output:
    if cursor["totalvotes"] == maximum_total_vote_increment:
        final_result.append({'timestamp': cursor["_id"].strftime("%Y-%m-%d %H:%M:%S"), 'TotIncrement': maximum_total_vote_increment})

for doc in final_result:
    print(doc)


