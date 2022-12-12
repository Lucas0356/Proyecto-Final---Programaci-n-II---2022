a = {
"users": [
{
    "id": 0,
    "username": "Juancito2001",
    "password": "messi",
    "contributions": None,
    "comments": 
        {
        "Spiderman-2": "i love spiderman",
        "One Piece Film: Red": "The best anime in the history"
        }
    },
    {
    "id": 1,
    "username": "RicarditoCABJ",
    "password": "bokitapasion",
    "contributions": None,
    "comments": [
        {
        "Sonic 2: The movie": "Sonic > Mario",
        "Dragon Ball Super Super Hero": "Piccolo is my favourite character in dragon ball world! ;)"
        }
    ]
    }
],
"films": [
    {
    "Sonic 2: The movie": [
    {
    "Year": "2022",
    "Director": "Jeff Fowler",
    "Gender": "Adventure/Comedy",
    "Synopsis": "Sonic y su compañero Tails emprenden un viaje alrededor del mundo en busca de una esmeralda que tiene del poder de destruir civilizaciones."
    }
    ]
}
]
}

x = len(a["users"])
usernames = []
i = 0
while i < x:
    usernames.append(a["users"][i]["username"])
    i= i + 1
print (usernames)