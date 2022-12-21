# Projet-GLO-4035

# ************DISCLAIMER SUR LE TEMPS DE BUILD *********

Après des heures et des heures d’essais avec les volumes de Docker, nous sommes totalement incapables de trouver une manière pour persister les données sans constamment repeupeler au moment de faire docker compose up. Dans tous nos essais, la base de donnée Neo4j était toujours vide. 

Cela a aussi GRANDEMENT compliqué les processus de développement … une tâche qui aurait du prendre quelques secondes prenait maintenant plusieurs dizaines de minutes (repeupalage, pas de mode debug, lag intense sur la VM du cours malgre beaucoup de ressources  …). …), donc la qualité du code et des requêtes (notamment pour GET/parcours) laisse à desirer.

Ainsi, …chaque Docker compose up est encore long, désolé (5 à 10 minutes en moyenne selon l’ordinateur …). Par contre, cela permet de montrer les requêtes que nous avons implémentées et le fonctionnement globale de l’application. 

Désolé pour cet inconvenient et nous espérons que cela ne vous nuira pas trop pour la correction.


## Requêtes

### GET /heartbeat

**Expected response format**
```
{
    "villeChoisie": str
}
```

**Response Exemple**
```json
{
    "villeChoisie": "Cornwall"
}
```

### GET /extracted_data

**Expected response format**
```
{
    "nbRestaurants": int,
    "nbSegments": int
}
```

**Response Exemple**
```json
{
    "nbRestaurants": 71,
    "nbSegments": 1904
}
```

### GET /transformed_data

**Expected Response format**
```
{
  "restaurants": {
  $type1: int ,
  $type2: int ,
  ...
},
  "longueurCyclable": float
}
```

**Response Exemple**
```json
{
    "longueurCyclable": 349560.5730000006,
    "restaurants": {
        "American (Traditional)": 3,
        "Asian Fusion": 1,
        "Bakeries": 1,
        "Barbeque": 1,
        "Bars": 1,
        "Beer Bar": 1,
        "Bistros": 1,
        "Breakfast & Brunch": 5,
        "Buffets": 1,
        "Burgers": 7,
        "Butcher": 1,
        "Cafes": 1,
        "Cambodian": 1,
        "Canadian (New)": 7,
        "Caribbean": 1,
        "Chicken Shop": 3,
        "Chicken Wings": 2,
        "Chinese": 4,
        "Coffee & Tea": 1,
        "Comfort Food": 1,
        "Delis": 3,
        "Desserts": 1,
        "Diners": 3,
        "Fast Food": 8,
        "Fish & Chips": 2,
        "Gastropubs": 1,
        "Greek": 2,
        "Grocery": 1,
        "Halal": 1,
        "Hot Dogs": 2,
        "Indian": 2,
        "Italian": 5,
        "Japanese": 1,
        "Lebanese": 1,
        "Mediterranean": 1,
        "Mexican": 1,
        "Middle Eastern": 1,
        "Modern European": 1,
        "Noodles": 2,
        "Patisserie/Cake Shop": 1,
        "Pizza": 18,
        "Pubs": 2,
        "Ramen": 1,
        "Restaurants": 1,
        "Salad": 2,
        "Sandwiches": 7,
        "Seafood": 3,
        "Soup": 2,
        "Sports Bars": 3,
        "Sri Lankan": 1,
        "Sushi Bars": 2,
        "Thai": 4,
        "Vegan": 1,
        "Vietnamese": 1
    }
}
```

### GET /readme

**Expected response**
README.md File

**Response Exemple**
This file

### GET /type

**Expected response format**
```
[
  str ,
  str ,
  str ,
  ...
]
```

**Response Exemple**
```
[
  "Modern European",
  "Pubs",
  "Breakfast & Brunch",
  "Bistros",
  "Gastropubs",
  "Thai",
  "Sports Bars",
  "Burgers",
  "Beer Bar",
  "Cambodian",
  "Italian",
  "Noodles",
  "Vietnamese",
  "Seafood",
  "Salad",
  "Fish & Chips",
  "Pizza",
  "Indian",
  "Sri Lankan",
  "Canadian (New)",
  "Greek",
  "Chinese",
  "Barbeque",
  "Chicken Shop",
  "Comfort Food",
  "Bars",
  "Fast Food",
  "Vegan",
  "Mexican",
  "Buffets",
  "American (Traditional)",
  "Sushi Bars",
  "Ramen",
  "Soup",
  "Sandwiches",
  "Butcher",
  "Grocery",
  "Halal",
  "Delis",
  "Restaurants",
  "Mediterranean",
  "Lebanese",
  "Caribbean",
  "Diners",
  "Hot Dogs",
  "Japanese",
  "Asian Fusion",
  "Middle Eastern",
  "Cafes",
  "Bakeries",
  "Patisserie/Cake Shop",
  "Coffee & Tea",
  "Desserts",
  "Chicken Wings"
]
```


### GET /starting_point

**Expected request payload**
```
{
  "length": int (en metre),
  "type": [
    str,
    str,
    ...
  ]
}
```

**Expected response**
```
{
  "startingPoint": {
    "type": "Point",
    "coordinates": [
      float , float
    ]
  }
}
```
**Response exemple**
```
{
    "starting_point": {
        "coordinates": [
            45.01561,
            -74.739338
        ],
        "type": "Point"
    }
}
```

### GET /parcours

**Expected request payload**

```
{
  "startingPoint": {
    "type": "Point",
    "coordinates": [
      float , float
    ]
  },
  "length": int (en metre),
  "numberOfStops": int ,
  "type": [
    str ,
    str ,
    ...
  ]
}
```

**Expected response format**
```
{
  "type": "FeatureCollection ",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [
          float , float
        ]
      },
      "properties": {
        "name": str ,
        "type": str
      }
    },
      ...,
    {
      "type": "Feature",
      "geometry": {
      "type": "MultiLineString ",
      "coordinates": [
        [
          [
            float , float
          ],
          [
            float , float
          ],
          [
            float , float
          ],
            ...
          ]
        ]
      },
      "properties": {
        "length": float (en metres)
      }
    }
  ]
}
```
**Response exemple**
```
{
    "features": [
        {
            "geometry": {
                "coordinates": [
                    45.020919,
                    -74.70385
                ],
                "type": "Point"
            },
            "properties": {
                "name": "McDonalds",
                "type": "Burger"
            },
            "type": "Feature"
        },
        {
            "geometry": {
                "coordinates": [
                    45.024237,
                    -74.714329
                ],
                "type": "Point"
            },
            "properties": {
                "name": "The Shack",
                "type": "Pizza"
            },
            "type": "Feature"
        },
        {
            "geometry": {
                "coordinates": [
                    45.019472,
                    -74.720799
                ],
                "type": "Point"
            },
            "properties": {
                "name": "Pacini",
                "type": "Italian"
            },
            "type": "Feature"
        },
        {
            "geometry": {
                "coordinates": [
                    [
                        [
                            45.020919,
                            -74.70385
                        ],
                        [
                            45.120919,
                            -74.80385
                        ]
                    ],
                    [
                        [
                            45.030986,
                            -74.70433
                        ],
                        [
                            45.129556,
                            -74.809486
                        ]
                    ],
                    [
                        [
                            45.028544,
                            -74.719083
                        ],
                        [
                            45.120919,
                            -74.810438
                        ]
                    ]
                ],
                "type": "MultiLineString"
            },
            "properties": {
                "length": 12345
            },
            "type": "Feature"
        }
    ],
    "type": "FeatureCollection"
}
```

