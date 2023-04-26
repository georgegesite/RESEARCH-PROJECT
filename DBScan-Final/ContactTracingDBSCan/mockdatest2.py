import random
import time
import json
from datetime import datetime, timedelta

# Set up random seed for consistent results
random.seed(42)

# Set up possible names
names = ["Abueva, Stephen, S.",
"Amang, Andrei Raphel, T.",
"Arcayena, Jhon Reyl",
"Balais, Mark Horace, B.",
"Canizares, Michael T",
"Ilogon, Peter Neil, I.",
"Ingente, Warren, L.",
"Lagamao, Alexis",
"Libardo, Nikko Glenn, F.",
"Montoya, Jester, A.",
"Peligrino, Niñolito, E.",
"Picato, Kevin Lloyd, J.",
"Pinar, King Emmanuele, T.",
"Ponce, Jairo, B.",
"Omac, Christian Zyrus, G.",
"Oppus, Aldrin, I.",
"Ranario, Carl Titus, L.",
"Rollin, John Mackenly, B.",
"Saligumba, Emmanuel Jr, P.",
"Suganob, Rogelio Jr., C.",
"Tabuzo, Ramel, J.",
"Toh, Ian Rafael, A.",
"Vallecera, Mel Vincent, B.",
"Yabo, Jojie, S.",
"Bulabos, Joanah May",
"Calotes, Lyza Mae, M.",
"Coca, Teresa Mae, H.",
"Cutanda, Angel Kristie, O.",
"Dano, Sheila Mae, B.",
"Daplin, Mylyn, P.",
"Esterado, Rica Noreen, T.",
"Granada, Jack Danielle, L.",
"Gucor, Danica Jeanne, M.",
"Lagunoy, Anne Lorainne, C.",
"Olajay, Jinnyrose, G.",
"Orot, Melanie, M.",
"Quiño, Devie Valerie, T.",
"Timbal, Margarita Shiela, B.",
"Abellana, Lord Kelvin",
"Anub, Jeremiah Rey",
"Añasco, Dolph Allyn",
"Bentulan, Vince Pierre",
"Catad, Niño Laurence",
"Enad, Lemuel Jay",
"Gesite, George",
"Gohil, Robert Kin T.",
"Laguitao, Jessie Ryle",
"Laureano, Bryan",
"Lofranco, Ruel Riego",
"Mendez, Kean",
"Napallacan, Franz Mark",
"Rebarbas, Rod Kristian",
"Respecia, Charles Rene",
"Ricafort, Chester John",
"Soria, Daniel",
"Tadle, Joel",
"Tan, Marl Kenneth",
"Andrade, Jhune Maureen",
"Bacol, Deannah May",
"Cabanillas, Jonnalyn",
"Cadeliña, Mary Ranive",
"Carias, Alyzza Mae",
"Caseñas, Jovihanni",
"Danila, Rogimie",
"Fullante, Jazmin Joy",
"Jabines, Jay Anne",
"Jotojot, Jelian Kate",
"Labonog, Ellah Mae",
"Lampios, Claire Ann",
"Mauro, Cielo Mae",
"Molina, Fritgil Mae",
"Reyes, Fatima",
"Tagadiad, Mae Abegail",
"Tangcawan, Jaquelyn",
"Amper, Bryan",
"Banol, Felipe Jr. S.",
"Bergado, Karle Mathew, G",
"Boyboy, Juvenar, Jr",
"Budiongan, Elvan",
"Dimalanta, Kerbin, S.",
"Ibale, Ronnie",
"Lagura, Lloyd",
"Lopena, Grant Gregory",
"Mahilum, Shin, L.",
"Opelinia, Prince Lonito, B.",
"Relampagos, Joseph Caesar, O.",
"Roperos, Jade Harris",
"Rubin, Daniel",
"Tampos, Clifford John",
"Valeroso, Kenneth Lorvic",
"Vertulfo, Christian Paul",
"Ylaya, John Friderick, S.",
"Amolato, Jeneveve, A.",
"Arcales, Klien",
"Auditor, Lutchel, C.",
"Barril, Cathlene",
"Cabahug, Rena Mae",
"Calzado, Ma. Crizel",
"Campeciño, Gecille Marie",
"Fullido, Zendy Shervyl, M.",
"Lim, Jossa, M.",
"Longos, Dharlean Jeaseari, F.",
"Malig-on, Ivy Crescel",
"Palingcod, Mary Joyce, E.",
"Perpetua, Crystel Jem, P.",
"Sandigan, Jermedita",]

# Set up possible room numbers
rooms = list(range(101, 111)) + list(range(201, 211)) + list(range(301, 311))

# Generate data
data = []
for i in range(90):
    # Set up ID
    id_num = 125 + i

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
    date = datetime(2023, 4, 26) + timedelta(days=random.choice([0, 1]))
    hour = random.randint(7, 20)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    transdate = date.replace(hour=hour, minute=minute, second=second).strftime("%Y-%m-%d %H:%M:%S")

    # Set up epoch
    epoch = int(time.mktime(time.strptime(transdate, "%Y-%m-%d %H:%M:%S")))

    # Set up room
    room = random.choice(rooms)

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
with open("mock_data.json", "w") as f:
    json.dump(data, f, indent=2)







