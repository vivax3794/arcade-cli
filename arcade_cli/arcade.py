from __future__ import annotations

import csv
from io import TextIOWrapper
from typing import List, Tuple, Dict

import jwt
import requests


Star = Tuple[float, float, int]


def store_stars_in_file(stars: List[Star], file: TextIOWrapper) -> None:
    writer = csv.writer(file, dialect="unix")

    for star in stars:
        writer.writerow(star)

def load_stars_from_file(file: TextIOWrapper) -> List[Star]:
    reader = csv.reader(file)
    
    stars = []
    for row in reader:
        x, y, type_ = row
        stars.append((float(x), float(y), int(type_)))
    
    return stars


def get_twitch_id_from_jwt(jwt_token: str) -> str:
    data = jwt.decode(jwt_token, options={"verify_signature": False})
    return data["opaque_user_id"]

def from_api_stars(data: List[Dict[str, float]]) -> List[Star]:
    return [
        (star["x"], star["y"], int(star["currentStar"]))
        for star in data
    ]

def to_api_stars(data: List[Star]) -> List[Dict[str, float]]:
    return [
        {"x": star[0], "y": star[1], "currentStar": float(star[2])}
        for star in data
    ]

def get_stars_from_bucket(jwt: str, bucket: int) -> List[Star] | str:
    data = {
        "jwt": jwt,
        "saveIndex": bucket
    }

    resp = requests.post("http://arcade-placement-tool.herokuapp.com/get/userStarSaveData", json=data)
    data = resp.json()

    if not data["success"]:
        return data["data"]

    return from_api_stars(data["data"]["data"])

def save_stars_to_bucket(jwt: str, bucket: int, stars: List[Star]) -> None:
    data = {
        "jwt": jwt,
        "saveIndex": bucket,
        "stars": to_api_stars(stars)
    }

    requests.post("https://arcade-placement-tool.herokuapp.com/send/toDatabase", json=data)

def draw_in_stars(jwt: str, stars: List[Star]) -> None:
    data = {
        "jwt": jwt,
        "stars": to_api_stars(stars)
    }

    requests.post("https://arcade-placement-tool.herokuapp.com/send/toStarField", json=data)