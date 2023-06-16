from pprint import pprint
import json

import requests
import folium
from geopy import distance

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

yendex_key="0a4c58c6-a58d-4c1b-8f12-395d7481f64c"

location=input("где вы находитесь: ")
coordinates=fetch_coordinates(yendex_key,location)
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
nearest_cafeshka=sorted(information, key=get_coffee_distance)

pprint(type(nearest_cafeshka))
pprint (nearest_cafeshka[0:5])



m = folium.Map(coordinates,zoom_start=13)
tooltip = "Click me!"

for cafeshki in nearest_cafeshka:
    folium.Marker(
        [cafeshki['latitude'],cafeshki['longitude']], popup=cafeshki['title'], tooltip=tooltip
        ).add_to(m)


m.save("index.html")




