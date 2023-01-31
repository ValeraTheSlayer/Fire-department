from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
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
        point_lat = request.POST.get('lat')
        point_long = request.POST.get('long')
        point_address = request.POST.get('address')
        point_comment = request.POST.get('user_comments')
        if point_type == 'fire':
            print('point_type: ', point_type)
        if point_type == 'hydrant':
            print('point_type: ', point_type)
        if point_type == 'secure_place':
            print('point_type: ', point_type)
        print('request_time_string: ', request_time_string)
        print('point_lat: ', point_lat)
        print('point_long: ', point_long)
        print('point_address: ', point_address)
        print('point_comment: ', point_comment)
    return HttpResponse('new point request was succesfully')
