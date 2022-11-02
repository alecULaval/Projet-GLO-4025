from dataclasses import dataclass


@dataclass
class Restaurant:
    type: str
    address: str
    name: str
    phone: str
    price: str
    price_range: str
    website: str
    url: str
    latitude: str
    longitude: str
