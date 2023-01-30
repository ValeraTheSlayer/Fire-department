from django.shortcuts import render
import json


def test(request):
    return render(request, 'event_map/test.html')


def test_ajax(request):
    if request.is_ajax and 'radio' in request.POST:
        values = json.loads(request.POST.get('radio'))
        print(values)

