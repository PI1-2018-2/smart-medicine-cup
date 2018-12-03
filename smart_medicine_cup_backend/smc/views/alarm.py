import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.http import HttpResponse

from ..models import User, Cup, Alarm, Record


@csrf_exempt
def register_info(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'wrong http method, use POST'}, status=405)

    if request.content_type != 'application/json':
        return JsonResponse({'error': 'wrong content-type, use application/json'}, status=415)

    try:
        data = json.loads(request.body)
        handler = get_event_handler(data['event'])
        response = handler(data)
    except KeyError as e:
        response = JsonResponse({'error': 'invalid Json, problem with key or value: ' + str(e)}, status=400)
    except json.decoder.JSONDecodeError:
        response = JsonResponse({'error': 'invalid Json'}, status=400)

    return response


def get_event_handler(event):
    handlers = {
        'registered': register_alarm,
        'taken': create_record,
        'not_taken': create_record,
        'cancelled': cancel_alarm
    }

    return handlers[event]


def register_alarm(data):
    if data['partition'] in range(1, 4+1):
        try:
            alarm = Alarm.objects.create(
                cup=Cup.objects.get(cup_id=data['id_cup']),
                partition=data['partition'],
                start_time=f"{data['alarm_info']['start']['hour']}:{data['alarm_info']['start']['minute']}:00",
                period=f"{data['alarm_info']['period']['hour']}:{data['alarm_info']['period']['minute']}:00",
                duration=data['alarm_info']['duration'],
                is_active=True,
            )
            create_record(data)
            return JsonResponse({'ok': 'Record saved!'}, status=201)
        except ObjectDoesNotExist:
            cup_id = data['id_cup']
            return JsonResponse({'error': f'cannot find cup with id {cup_id}'}, status=404)

    return JsonResponse({'error': 'partition not in valid range [1,4]'}, status=400)


def cancel_alarm(data):
    response = create_record(data)
    if response.status_code == 201: # So alarm exists
        alarm = get_alarm(data)
        alarm.is_active = False
        alarm.save()
    return response


def get_alarm(data):
    alarms = Alarm.objects.filter(cup__cup_id=data['id_cup'], partition=data['partition'])
    if alarms:
        alarm = alarms.last()
        return alarm
    return None


def create_record(data):
    alarm = get_alarm(data)
    if alarm:
        Record.objects.create(alarm=alarm, cup_id=data['id_cup'], event=data['event'], moment=data['moment'])
        return JsonResponse({'ok': 'Record saved!'}, status=201)
    return JsonResponse({'error': "Cannot find alarm to cup '{id_cup}' and partition '{partition}'".format(**data)}, status=404)

@csrf_exempt
def get_record(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'wrong http method, use GET'}, status=405)
    
    data = Record.objects.all().values()
    data_list = list(data)
    return JsonResponse(data_list, safe=False)


@csrf_exempt
def get_contact(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'wrong http method, use GET'}, status=405)

    data = Cup.objects.all().values()
    data_list = list(data)
    return JsonResponse(data_list, safe=False)