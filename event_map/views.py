from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
from .models import Hydrants, FireHistory, SecurePlaces, \
                        Polygon_1_Coordinates, \
                        Polygon_2_Coordinates,\
                        Polygon_3_Coordinates,\
                        Polygon_4_Coordinates
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from decimal import Decimal
from yandex_geocoder import Client
import numpy as np
import json
import requests


def points_map(request):
    return render(request, 'event_map/points_map.html')


def new_point(request):
    if (request.method == 'POST') and ('point_type' in request.POST):
        now = datetime.now()
        request_time_string = now.strftime("%Y-%m-%d %H:%M:%S")
        point_type = request.POST.get('point_type')
        point_lat = float(request.POST.get('lat'))
        point_long = float(request.POST.get('long'))
        point_address = request.POST.get('address')
        user_comments = request.POST.get('user_comments')
        if point_type == 'fire':
            FireHistory.objects.create(
                event_date=now,
                user_comments=user_comments,
                latitude=point_lat,
                longitude=point_long,
                raw_address=point_address,
            )
        if point_type == 'hydrant':
            Hydrants.objects.create(
                created_date=now,
                user_comments=user_comments,
                latitude=point_lat,
                longitude=point_long,
                raw_address=point_address,
                working=True,
                )
        if point_type == 'secure_place':
            SecurePlaces.objects.create(
                created_date=now,
                user_comments=user_comments,
                latitude=point_lat,
                longitude=point_long,
                raw_address=point_address,
            )
    return HttpResponse('new point request was succesfully')


def history_points(request):
    #FireHistory.objects.all().delete()
    #Hydrants.objects.all().delete()
    #SecurePlaces.objects.all().delete()
    if (request.method == 'POST') and ('type_of_points' in request.POST):
        requested_type = request.POST.get('type_of_points')
        if requested_type == 'all':
            fire_response_list = []
            id_ = 0
            fire_event_list = FireHistory.objects.all()
            for fire_point in fire_event_list:
                fire_point_dict = {"type": "Feature",
                                   "id": id_,
                                   "geometry": {"type": "Point",
                                                "coordinates": [fire_point.latitude, fire_point.longitude]},
                                   "properties": {"balloonContentHeader": 'Пожар',
                                                  "balloonContentBody": f"<b>Адрес:</b>  {fire_point.raw_address} <br/> <b>Примечание: </b>  {fire_point.user_comments}",
                                                   "balloonContentFooter": f"<b>Дата:</b>{fire_point.event_date}",
                                                   "hintContent": 'Подробности метки пожар',
                                                   },
                                   "options": {"iconLayout": 'default#image',
                                               "iconImageHref": "http://192.168.88.252/static/images/fire.png"
                                                },
                                    }
                fire_response_list.append(fire_point_dict)
                id_ += 1

            hydrant_response_list = []
            hydrant_event_list = Hydrants.objects.all()
            for hydrant_point in hydrant_event_list:
                hydrant_point_dict = {"type": "Feature",
                                   "id": id_,
                                   "geometry": {"type": "Point",
                                                "coordinates": [hydrant_point.latitude, hydrant_point.longitude]},
                                   "properties": {"balloonContentHeader": 'Гидрант',
                                                  "balloonContentBody": f"<b>Адрес:</b>  {hydrant_point.raw_address} <br/> <b>Примечание: </b>  {hydrant_point.user_comments}",
                                                   "balloonContentFooter": f"<b>Дата:</b>{hydrant_point.created_date}",
                                                   "hintContent": 'Подробности метки Гидрант',
                                                   },
                                   "options": {"iconLayout": 'default#image',
                                               "iconImageHref": "http://192.168.88.252/static/images/hydrant1.png"
                                                },
                                    }
                hydrant_response_list.append(hydrant_point_dict)
                id_ += 1

            secure_response_list = []
            secure_event_list = SecurePlaces.objects.all()
            for secure_point in secure_event_list:
                secure_point_dict = {"type": "Feature",
                                      "id": id_,
                                      "geometry": {"type": "Point",
                                                   "coordinates": [secure_point.latitude, secure_point.longitude]},
                                      "properties": {"balloonContentHeader": 'Объект повыщеной степени риска',
                                                     "balloonContentBody": f"<b>Адрес:</b>  {secure_point.raw_address} <br/> <b>Примечание: </b>  {secure_point.user_comments}",
                                                     "balloonContentFooter": f"<b>Дата:</b>{secure_point.created_date}",
                                                     "hintContent": 'Подробности метки Гидрант',
                                                     },
                                      "options": {"iconLayout": 'default#image',
                                                  "iconImageHref": "http://192.168.88.252/static/images/home.png"
                                                  },
                                      }
                secure_response_list.append(secure_point_dict)
                id_ += 1

            hydrant_fire_secure_event_dict = {'type': "FeatureCollection",
                                      "features": hydrant_response_list+fire_response_list+secure_response_list}
            hydrant_event_secure_response = json.dumps(hydrant_fire_secure_event_dict)
            return HttpResponse(hydrant_event_secure_response, content_type="application/json")


def get_polygon_1_points(request):
    if request.method == 'POST' and 'update_polygon_1_points' in request.POST:
        Polygon_1_Coordinates.objects.all().delete()
        for id_ in range(1, len(request.POST)):
            point = request.POST.get(f'{id_}')
            point_lat = float(point.split(',')[0])
            point_long = float(point.split(',')[1])
            Polygon_1_Coordinates.objects.create(
                latitude=point_lat,
                longitude=point_long,
                )
        return HttpResponse('get_polygon_1_points success')
    if request.method == 'GET':
        polygon_1_coordinates = Polygon_1_Coordinates.objects.all()
        polygon_1_coordinates_dict = {}
        id_ = 0
        for point in polygon_1_coordinates:
            latitude = point.latitude
            longitude = point.longitude
            polygon_1_coordinates_dict[id_] = {'latitude': latitude,
                                               'longitude': longitude}
            id_ += 1
        polygon_1_coordinates_json = json.dumps(polygon_1_coordinates_dict)
        return HttpResponse(polygon_1_coordinates_json, content_type="application/json")


def get_polygon_2_points(request):
    if request.method == 'POST' and 'update_polygon_2_points' in request.POST:
        Polygon_2_Coordinates.objects.all().delete()
        for id_ in range(1, len(request.POST)):
            point = request.POST.get(f'{id_}')
            point_lat = float(point.split(',')[0])
            point_long = float(point.split(',')[1])
            Polygon_2_Coordinates.objects.create(
                latitude=point_lat,
                longitude=point_long,
                )
        return HttpResponse('get_polygon_2_points success')
    if request.method == 'GET':
        polygon_2_coordinates = Polygon_2_Coordinates.objects.all()
        polygon_2_coordinates_dict = {}
        id_ = 0
        for point in polygon_2_coordinates:
            latitude = point.latitude
            longitude = point.longitude
            polygon_2_coordinates_dict[id_] = {'latitude': latitude,
                                               'longitude': longitude}
            id_ += 1
        polygon_2_coordinates_json = json.dumps(polygon_2_coordinates_dict)
        return HttpResponse(polygon_2_coordinates_json, content_type="application/json")
    return HttpResponse('empty')


def get_polygon_3_points(request):
    if request.method == 'POST' and 'update_polygon_3_points' in request.POST:
        Polygon_3_Coordinates.objects.all().delete()
        for id_ in range(1, len(request.POST)):
            point = request.POST.get(f'{id_}')
            point_lat = float(point.split(',')[0])
            point_long = float(point.split(',')[1])
            Polygon_3_Coordinates.objects.create(
                latitude=point_lat,
                longitude=point_long,
                )
        return HttpResponse('get_polygon_3_points success')
    if request.method == 'GET':
        polygon_3_coordinates = Polygon_3_Coordinates.objects.all()
        polygon_3_coordinates_dict = {}
        id_ = 0
        for point in polygon_3_coordinates:
            latitude = point.latitude
            longitude = point.longitude
            polygon_3_coordinates_dict[id_] = {'latitude': latitude,
                                               'longitude': longitude}
            id_ += 1
        polygon_3_coordinates_json = json.dumps(polygon_3_coordinates_dict)
        return HttpResponse(polygon_3_coordinates_json, content_type="application/json")
    return HttpResponse('empty')


def get_polygon_4_points(request):
    if request.method == 'POST' and 'update_polygon_4_points' in request.POST:
        Polygon_4_Coordinates.objects.all().delete()
        for id_ in range(1, len(request.POST)):
            point = request.POST.get(f'{id_}')
            point_lat = float(point.split(',')[0])
            point_long = float(point.split(',')[1])
            Polygon_4_Coordinates.objects.create(
                latitude=point_lat,
                longitude=point_long,
                )
        return HttpResponse('get_polygon_4_points success')
    if request.method == 'GET':
        polygon_4_coordinates = Polygon_4_Coordinates.objects.all()
        polygon_4_coordinates_dict = {}
        id_ = 0
        for point in polygon_4_coordinates:
            latitude = point.latitude
            longitude = point.longitude
            polygon_4_coordinates_dict[id_] = {'latitude': latitude,
                                               'longitude': longitude}
            id_ += 1
        polygon_4_coordinates_json = json.dumps(polygon_4_coordinates_dict)
        return HttpResponse(polygon_4_coordinates_json, content_type="application/json")
    return HttpResponse('empty')


def get_department(request):
    point_type = request.POST.get('point_type')
    polygon_1_coordinates = Polygon_1_Coordinates.objects.all()
    polygon_1_coordinates_list = []

    polygon_2_coordinates = Polygon_2_Coordinates.objects.all()
    polygon_2_coordinates_list = []

    polygon_3_coordinates = Polygon_3_Coordinates.objects.all()
    polygon_3_coordinates_list = []

    polygon_4_coordinates = Polygon_4_Coordinates.objects.all()
    polygon_4_coordinates_list = []

    for point in polygon_1_coordinates:
        latitude = point.latitude
        longitude = point.longitude
        polygon_1_coordinates_list.append([longitude, latitude])

    for point in polygon_2_coordinates:
        latitude = point.latitude
        longitude = point.longitude
        polygon_2_coordinates_list.append([longitude, latitude])

    for point in polygon_3_coordinates:
        latitude = point.latitude
        longitude = point.longitude
        polygon_3_coordinates_list.append([longitude, latitude])

    for point in polygon_4_coordinates:
        latitude = point.latitude
        longitude = point.longitude
        polygon_4_coordinates_list.append([longitude, latitude])

    polygon_1_coordinates_list_np = np.array(polygon_1_coordinates_list)
    polygon_2_coordinates_list_np = np.array(polygon_2_coordinates_list)
    polygon_3_coordinates_list_np = np.array(polygon_3_coordinates_list)
    polygon_4_coordinates_list_np = np.array(polygon_4_coordinates_list)

    polygon_1 = Polygon(polygon_1_coordinates_list_np)
    polygon_2 = Polygon(polygon_2_coordinates_list_np)
    polygon_3 = Polygon(polygon_3_coordinates_list_np)
    polygon_4 = Polygon(polygon_4_coordinates_list_np)

    if request.method == 'POST' and 'get_department' == point_type:
        point_latitude = request.POST.get('lat')
        point_longitude = request.POST.get('long')
        check_point = Point(point_longitude, point_latitude)
        print('map', point_longitude, point_latitude)

        if check_point.within(polygon_1):

            return HttpResponse('Область СПЧ-1')
        if check_point.within(polygon_2):
            return HttpResponse('Область СПЧ-2')
        if check_point.within(polygon_3):
            return HttpResponse('Область СПЧ-3')
        if check_point.within(polygon_4):
            return HttpResponse('Область СПЧ-4')

        return HttpResponse('Не входит в ДЧС города Тараз')
    if request.method == 'POST' and 'get_department_card' == point_type:
        address_string = request.POST.get('address')
        apikey = "81c87445-f1fe-4e16-8b33-c83baf78e8f2"
        coordinates = fetch_coordinates(apikey, address_string)
        point_latitude = float(coordinates[0])
        point_longitude = float(coordinates[1])
        print('card ', address_string , point_longitude, point_latitude)
        check_point = Point(point_latitude, point_longitude)
        if check_point.within(polygon_1):
            department_dict = {'latitude': latitude,
                               'longitude': longitude,
                               'department_text': 'Область СПЧ-1'}
            department_json = json.dumps(department_dict)
            return HttpResponse(department_json, content_type="application/json")
        if check_point.within(polygon_2):
            department_dict = {'latitude': latitude,
                               'longitude': longitude,
                               'department_text': 'Область СПЧ-2'}
            department_json = json.dumps(department_dict)
            return HttpResponse(department_json, content_type="application/json")
        if check_point.within(polygon_3):
            department_dict = {'latitude': latitude,
                               'longitude': longitude,
                               'department_text': 'Область СПЧ-3'}
            department_json = json.dumps(department_dict)
            return HttpResponse(department_json, content_type="application/json")
        if check_point.within(polygon_4):
            department_dict = {'latitude': latitude,
                               'longitude': longitude,
                               'department_text': 'Область СПЧ-4'}
            department_json = json.dumps(department_dict)
            return HttpResponse(department_json, content_type="application/json")
        department_dict = {'latitude': latitude,
                           'longitude': longitude,
                           'department_text': 'Не входит в ДЧС города Тараз'}
        department_json = json.dumps(department_dict)
        return HttpResponse(department_json, content_type="application/json")
        #coordinates = client.coordinates("Казахстан Тараз Толе-би 19")


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
    return lon, lat