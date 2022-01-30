from __future__ import annotations

import csv
from io import TextIOWrapper
from typing import TYPE_CHECKING

import jwt
import requests

if TYPE_CHECKING:
    from typing import TypeAlias


Star: TypeAlias = tuple[float, float, int]


NGROK_URL = "https://raw.githubusercontent.com/MatissesProjects/matissesprojects.github.io/master/CNAME"


def get_ngrok() -> str:
    resp = requests.get(NGROK_URL)
    return resp.text

def store_stars_in_file(stars: list[Star], file: TextIOWrapper) -> None:
    writer = csv.writer(file, dialect="unix")

    for star in stars:
        writer.writerow(star)

def load_stars_from_file(file: TextIOWrapper) -> list[Star]:
    reader = csv.reader(file)
    
    stars = []
    for row in reader:
        x, y, type_ = row
        stars.append((float(x), float(y), int(type_)))
    
    return stars


def get_twitch_id_from_jwt(jwt_token: str) -> str:
    data = jwt.decode(jwt_token, options={"verify_signature": False})
    return data["opaque_user_id"]

def from_api_stars(data: list[dict[str, float]]) -> list[Star]:
    return [
        (star["x"], star["y"], int(star["currentStar"]))
        for star in data
    ]

def to_api_stars(data: list[Star]) -> list[dict[str, float]]:
    return [
        {"x": star[0], "y": star[1], "currentStar": float(star[2])}
        for star in data
    ]

def get_stars_from_bucket(jwt: str, bucket: int) -> list[Star]:
    data = {
        "jwt": jwt,
        "saveIndex": bucket
    }

    resp = requests.post("http://arcade-placement-tool.herokuapp.com/get/userStarSaveData", json=data)
    data = resp.json()

    return from_api_stars(data["data"]["data"])

def save_stars_to_bucket(jwt: str, bucket: int, stars: list[Star]) -> None:
    data = {
        # "twitchId": get_twitch_id_from_jwt(jwt),
        "jwt": jwt,
        "saveIndex": bucket,
        "stars": to_api_stars(stars)
    }

    requests.post("https://arcade-placement-tool.herokuapp.com/send/toDatabase", json=data)

def draw_in_stars(jwt: str, stars: list[Star]) -> None:
    data = {
        "jwt": jwt,
        "stars": to_api_stars(stars)
    }

    requests.post("https://arcade-placement-tool.herokuapp.com/send/toStarField", json=data)