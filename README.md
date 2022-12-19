# Projet-GLO-4035

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
**Response Exemple**

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

