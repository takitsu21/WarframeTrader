import numpy as np
from matplotlib import pyplot as plt
from api_response import *
import time, datetime

# d2 = datetime.datetime.strptime(ts[:len(ts)-19],"%Y-%m-%d")

api = WfmApi("items", "ash_prime_blueprint", "statistics")
data = run(api.data())
x, y, z = [], [], []
acc = 0
for stats in data["payload"]["statistics_live"]["90days"]:
    if stats["order_type"] == "sell":
        ddate_f = stats["datetime"][:len(stats["datetime"])-19]
        ddate_plan = datetime.datetime.strptime(ddate_f,"%Y-%m-%d")
        x.append(str(ddate_plan.day) +"/"+ str(ddate_plan.month))#
        y.append(stats["avg_price"])
    else: #make buyer avg price
        z.append(stats["avg_price"])

plt.plot(x, y)
plt.plot(x, z)
plt.legend(["Seller", "Buyer"])
plt.xlabel("Time")
plt.ylabel("Platinum")

plt.show()

#     api = WfmApi("items", "ash_prime_blueprint", "statistics")
#     print(json.dumps(run(api.data()), indent=4))