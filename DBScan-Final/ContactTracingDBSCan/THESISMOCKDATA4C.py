import random
import time
import json
from datetime import datetime, timedelta

# Set up random seed for consistent results
random.seed(42)

# Set up possible names
names = ["Tampos, Clifford John", "Barril, Cathlene", "Rubin, Daniel","Banol, Felipe Jr. S.","Roperos, Jade Harris","Bergado, Karle Mathew","Ylaya, John Friderick",
"Valeroso, Kenneth Lorvic","Dimalanta, Kerbin", "Arcales, Klien", "Lagura, Lloyd", "Cabahug, Rena Mae", "Lim, Jossa", "Vertulfo, Christian Paul","Ibale, Ronnie",
"Calzado, Ma. Crizel", "Budiongan, Elvan", "Amper, Bryan"
]

for i in range(876):
    random.shuffle(names)

data = []
for i in range(18):
    # Set up ID
    id_num = 433 + i


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
    date = datetime(2023, 4, 27)
    hour = 4
    minute = random.randint(0, 45)
    second = random.randint(0, 59)
    transdate = date.replace(hour=hour, minute=minute, second=second).strftime("%Y-%m-%d %H:%M:%S")


    epoch = int(time.mktime(time.strptime(transdate, "%Y-%m-%d %H:%M:%S")))

    # Set up room
    room = 110

    temp = round(random.normalvariate(36.5, 0.5), 2)
    course = "BSCPE 4C"


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
with open("sched17_4c.json", "w") as f:
    json.dump(data, f, indent=2)
