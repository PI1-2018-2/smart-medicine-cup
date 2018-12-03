import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

from ..models import User, Cup, Contact, Alarm, Record


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
            alarm = Alarm(
                cup=Cup.objects.get(id=data['id_cup']),
                partition=data['partition'],
                start_time=f"{data['alarm_info']['start']['hour']}:{data['alarm_info']['start']['minute']}:00",
                period=f"{data['alarm_info']['period']['hour']}:{data['alarm_info']['period']['minute']}:00",
                duration=data['alarm_info']['duration'],
                is_active=True,
            )
            alarm.save()
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'cannot find cup with this id'}, status=404)

        return create_record(data)
    return JsonResponse({'error': 'partition not in valid range [1,4]'}, status=400)


def cancel_alarm(data):
    alarms = Alarm.objects.filter(cup=data['id_cup'], partition=data['partition'])

    if alarms:
        alarm = alarms.last()
        alarm.is_active = False
        alarm.save()

        return create_record(data)
    return JsonResponse({'error': "Cannot find alarm to cup '{id_cup}' and partition '{partition}'".format(**data)}, status=404)


def create_record(data, alarm):
    Record.objects.create(alarm=alarm, cup_id=data['id_cup'], event=data['event'], moment=data['moment'])
    return JsonResponse({'ok': 'Record saved!'}, status=201)
