from dataclasses import dataclass


@dataclass
class Restaurant:
    id: str
    type: list
    address: str
    name: str
    latitude: str
    longitude: str
