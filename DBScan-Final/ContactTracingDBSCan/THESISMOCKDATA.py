import random
import time
import json
from datetime import datetime, timedelta

# Set up random seed for consistent results
random.seed(42)

# Set up possible names
names = [
"Gesite, George",
"Gohil, Robert Kin",
# "Jotojot, Jelian Kate",
# "Lampios, Claire Ann",

]

for i in range(666):
    random.shuffle(names)

data = []
for i in range(2):
    # Set up ID
    id_num = 493 + i


    if len(names) > 0:
        if i < 66:
            name = random.choice(names)
        elif i < 88:
            name = random.choice([n for n in names if names.count(n) < 2])
        else:
            name = random.choice(names)
        names.remove(name)
    else:
        name = "Unknown"

    # Set up transaction date
    date = datetime(2023, 5, 4)
    hour = 8
    minute = random.randint(30, 45)
    second = random.randint(0, 59)
    transdate = date.replace(hour=hour, minute=minute, second=second).strftime("%Y-%m-%d %H:%M:%S")


    epoch = int(time.mktime(time.strptime(transdate, "%Y-%m-%d %H:%M:%S")))

    # Set up room
    room = 9

    temp = round(random.normalvariate(36.5, 0.5), 2)
    course = "BSCPE 4A"


    data.append({
        "id": id_num,
        "name": name,
        "transdate": transdate,
        "epoch": epoch,
        "room": room,
        "temp": f"{temp} C",
        "course": course
    })

# Write data to file
with open("actual1.json", "w") as f:
    json.dump(data, f, indent=2)
