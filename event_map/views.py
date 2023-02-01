from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
from .models import Hydrants, FireHistory, SecurePlaces, \
                        Polygon_1_Coordinates, \
                        Polygon_2_Coordinates,\
                        Polygon_3_Coordinates,\
                        Polygon_4_Coordinates
import json


def test(request):
    return render(request, 'event_map/oper_map.html')


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
                                               "iconImageHref": "http://localhost/static/images/fire.png"
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
                                               "iconImageHref": "http://localhost/static/images/hydrant1.png"
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
                                                  "iconImageHref": "http://localhost/static/images/home.png"
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
        print('len-', len(request.POST))
        for id_ in range(1, len(request.POST)):
            point = request.POST.get(f'{id_}')
            point_lat = float(point.split(',')[0])
            point_long = float(point.split(',')[1])
            print(id_, '-', point_lat, point_long)
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
        print(polygon_1_coordinates_dict)
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
        print(polygon_2_coordinates_dict)
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
            print(point_long, point_long)
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