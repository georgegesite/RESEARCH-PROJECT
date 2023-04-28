import random
import time
import json
from datetime import datetime, timedelta

# Set up random seed for consistent results
random.seed(42)

# Set up possible names
names = [
"Abellana, Lord Kelvin",
"Anub, Jeremiah Rey",
"Anasco, Dolph Allyn",
"Bentulan, Vince Pierre",
"Catad, Nino Laurence",
"Enad, Lemuel Jay",
"Gesite, George Jr C.",
"Gohil, Robert Kin T.",
"Laguitao, Jessie Ryle",
"Laureano, Bryan",
"Lofranco, Ruel Riego",
"Mendez, Kean",
"Napallacan, Franz Mark",
"Rebarbas, Rod Kristian",
"Respecia, Charles Rene",
"Soria, Daniel",
"Tadle, Joel",
"Tan, Marl Kenneth",
"Bacol, Deannah May",
"Cabanillas, Jonnalyn",
"Cadelina, Mary Ranive",
"Carias, Alyzza Mae",
"Casenas, Jovihanni",
"Danila, Rogimie",
"Fullante, Jazmin Joy",
"Jabines, Jay Anne",
"Jotojot, Jelian Kate",
"Labonog, Ellah Mae",
"Lampios, Claire Ann",
"Mauro, Cielo Mae",
"Molina, Fritgil Mae",
"Tagadiad, Mae Abegail",
"Tangcawan, Jaquelyn",
]
random.shuffle(names)
# Set up possible room numbers


# Generate data
data = []
for i in range(30):
    # Set up ID
    id_num = 333 + i

    # Set up name
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
    date = datetime(2023, 4, 28)
    hour = 5
    minute = random.randint(15, 45)
    second = random.randint(0, 59)
    transdate = date.replace(hour=hour, minute=minute, second=second).strftime("%Y-%m-%d %H:%M:%S")

    # Set up epoch
    epoch = int(time.mktime(time.strptime(transdate, "%Y-%m-%d %H:%M:%S")))

    # Set up room
    room = 205

    # Set up temperature
    temp = round(random.normalvariate(36.5, 0.5), 2)
    course = "BSCPE 4A"

    # Append to data list
    data.append({
        "id": id_num,
        "name": name,
        "transdate": transdate,
        "epoch": epoch,
        "room": room,
        "temp": f"{temp} C\r\n",
        "course": course
    })

# Write data to file
with open("sched12.json", "w") as f:
    json.dump(data, f, indent=2)
