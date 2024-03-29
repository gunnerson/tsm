import requests
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
import hashlib
import hmac
import json

from .models import Truck, Company


def get_vehicles_locations(id):
    url = "https://api.keeptruckin.com/v1/vehicle_locations?vehicle_ids={0}&per_page=25&page_no=1".format(
        id)
    headers = {
        "Accept": "application/json",
        "X-Api-Key": settings.GOMOTIVE_API_KEY,
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    context = {}
    try:
        context['odometer'] = int(data["vehicles"][0]["vehicle"]
                                  ["current_location"].get("odometer"))
        context['lon'] = data["vehicles"][0]["vehicle"]["current_location"].get(
            "lon")
        context['lat'] = data["vehicles"][0]["vehicle"]["current_location"].get(
            "lat")
        context['bearing'] = get_bearing(
            data["vehicles"][0]["vehicle"]["current_location"].get("bearing"))
        context['desc'] = data["vehicles"][0]["vehicle"]["current_location"].get(
            "description")
        context['driver'] = (data["vehicles"][0]["vehicle"]["current_driver"].get("first_name")
                             + ' ' + data["vehicles"][0]["vehicle"]["current_driver"].get("last_name")).title()
    except (IndexError, TypeError, AttributeError):
        pass
    return context


def get_vehicle(id):
    url = "https://api.keeptruckin.com/v1/vehicles/{0}".format(id)
    headers = {
        "Accept": "application/json",
        "X-Api-Key": settings.GOMOTIVE_API_KEY,
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    context = {}
    context['number'] = data["vehicle"].get("number")
    context['vin'] = data["vehicle"].get("vin")
    context['make'] = data["vehicle"].get("make")
    context['model'] = data["vehicle"].get("model")
    context['year'] = data["vehicle"].get("year")
    context['eld_id'] = data["vehicle"]["eld_device"].get("id")
    return context


def get_fault_codes(id):
    url = "https://api.keeptruckin.com/v1/fault_codes?eld_device_ids=&vehicle_ids={0}&status=open&per_page=25&page_no=1".format(
        id)
    headers = {
        "Accept": "application/json",
        "X-Api-Key": settings.GOMOTIVE_API_KEY,
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    context = []
    for i in range(0, data["total"], 1):
        try:
            fault_code = {}
            fault_code_data = data['fault_codes'][i].get('fault_code')
            if fault_code_data:
                fault_code['code_label'] = fault_code_data.get('code_label').replace(
                    '-', ' ')
                fault_code['fmi'] = fault_code_data.get('fmi')
                fault_code['code_description'] = fault_code_data.get(
                    'code_description')
                fault_code['source'] = fault_code_data.get(
                    'source_address_label')
                fault_code['first_observed_at'] = fault_code_data.get('first_observed_at').replace(
                    'T', ' ').replace('Z', '')
                fault_code['last_observed_at'] = fault_code_data.get('last_observed_at').replace(
                    'T', ' ').replace('Z', '')
                context.append(fault_code)
        except (KeyError, IndexError):
            pass
    return context


def get_bulk_vehicles_locations():
    ours = Company.objects.filter(id__in=[1, 2])
    trucks = Truck.objects.filter(owner__in=ours, show=True)
    ids = ''
    for t in trucks:
        if t.kt_id:
            ids += 'vehicle_ids[]={0}&'.format(t.kt_id)
    url = "https://api.keeptruckin.com/v1/vehicle_locations?{0}&per_page=50&page_no=1".format(
        ids)
    headers = {
        "Accept": "application/json",
        "X-Api-Key": settings.GOMOTIVE_API_KEY,
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    context = []
    for i in range(0, data["pagination"]["total"], 1):
        try:
            vehicle = {}
            vehicle_data = data["vehicles"][i].get("vehicle")
            location_data = vehicle_data.get("current_location")
            if vehicle_data:
                vehicle['number'] = vehicle_data.get("number")
                truck = trucks.get(kt_id=int(vehicle_data.get("id")))
                vehicle['truck'] = truck.id
            if location_data:
                vehicle['lat'] = location_data.get("lat")
                vehicle['lon'] = location_data.get("lon")
                vehicle['bearing'] = location_data.get("bearing")
            context.append(vehicle)
        except (KeyError, IndexError):
            pass
    return context


def get_update_odometers():
    ours = Company.objects.filter(id__in=[1, 2])
    trucks = Truck.objects.filter(owner__in=ours)
    ids = ''
    for t in trucks:
        if t.kt_id:
            ids += 'vehicle_ids[]={0}&'.format(t.kt_id)
    url = "https://api.keeptruckin.com/v1/vehicle_locations?{0}&per_page=50&page_no=1".format(
        ids)
    headers = {
        "Accept": "application/json",
        "X-Api-Key": settings.GOMOTIVE_API_KEY,
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    for i in range(0, data["pagination"]["total"], 1):
        try:
            truck = trucks.get(kt_id=data["vehicles"][i]["vehicle"]["id"])
            truck.odometer = int(data["vehicles"][i]["vehicle"]
                                 ["current_location"]["odometer"])
            truck.save(update_fields=['odometer'])
        except (KeyError, TypeError):
            pass
    return True


@ csrf_exempt
def gomotive_webhook(request):
    payload = request.body
    digester = hmac.new(str.encode(
        settings.GOMOTIVE_ENDPOINT_SECRET), payload, hashlib.sha1)
    if digester.hexdigest() != request.headers['X-KT-Webhook-Signature']:
        raise PermissionDenied
    else:
        data = json.loads(payload)
        try:
            truck = Truck.objects.get(kt_id=data['vehicle_id'])
            truck.odometer = int(data['odometer'])
            truck.save(update_fields=['odometer'])
        except (ObjectDoesNotExist, TypeError):
            pass
    return HttpResponse('')


def get_bearing(b):
    if b >= 337.5 or b < 22.5:
        return 'N'
    elif b >= 22.5 and b < 67.5:
        return 'NE'
    elif b >= 67.5 and b < 112.5:
        return 'E'
    elif b >= 112.5 and b < 157.5:
        return 'SE'
    elif b >= 157.5 and b < 202.5:
        return 'S'
    elif b >= 202.5 and b < 247.5:
        return 'SW'
    elif b >= 247.5 and b < 292.5:
        return 'W'
    elif b >= 292.5 and b < 337.5:
        return 'NW'
    else:
        return None
