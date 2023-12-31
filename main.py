import os
from pprint import pprint
import json

import requests
import folium
from geopy import distance
from dotenv import load_dotenv

load_dotenv()


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lat, lon


#открывает файл,достает все содержимое и это все в переменной file_contents
with open("coffee.json", "r") as my_file:
    file_contents = my_file.read()
    file_contents = json.loads(file_contents)

print ("ПРИВЕТ! ТЫ ПОПАЛ НА СЕРВЕР МАЙНКРАФТА! ПИШИ НОМЕР КАРТЫ И СВОЕ МЕСТОПОЛОЖЕНИЕ, И ПОЛУЧИ В ПОДАРОК 5  DUNGEON МАСТЕРОВ ДОМОЙ")

yandex_key=os.getenv("YANDEX_KEY")

location=input("где вы находитесь: ")
coordinates=fetch_coordinates(yandex_key,location)
print=("ваши координаты: ",coordinates)

information=[]
for coffee in file_contents:
    cofeshki={
        "title":coffee ['Name'],
        "latitude":coffee ['Latitude_WGS84'],
        "longitude":coffee ['Longitude_WGS84'],
        "distance":distance.distance((coffee ['Latitude_WGS84'],coffee ['Longitude_WGS84']), coordinates ).km
        }
    information.append(cofeshki)
def get_coffee_distance(coffee):
    return coffee['distance']
distance_sorted_cafeshki=sorted(information, key=get_coffee_distance)


m = folium.Map(coordinates,zoom_start=13)
tooltip = "Click me!"

for cafeshki in distance_sorted_cafeshki[0:5]:
    folium.Marker(
        [cafeshki['latitude'],cafeshki['longitude']], popup=cafeshki['title'], tooltip=tooltip
        ).add_to(m)


m.save("index.html")




