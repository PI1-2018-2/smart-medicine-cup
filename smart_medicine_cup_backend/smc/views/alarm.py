import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

from ..models import User, Cup, Contact, Alarm, Record


@csrf_exempt
def register_info(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'wrong method, use POST'}, status=405)

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
        'taken': update_record,
        'not_taken': alert_contact,
        'cancelled': cancel_alarm
    }

    return handlers[event]


def register_alarm(data):
    if data['partition'] > 4 or data['partition'] < 1:
        return JsonResponse({'error': 'wrong partition range'}, status=400)

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

    alarm_record = Record(
        alarm=alarm,
        event=data['event'],
        moment=data['moment']
    )
    alarm_record.save()

    return JsonResponse({'ok': 'Register saved!'}, status=201)


def cancel_alarm(data):
    alarm = Alarm.objects.filter(cup=data['id_cup'], partition=data['partition']).last()

    if alarm:
        alarm.is_active = False
        alarm.save()
        update_record(data)
        return JsonResponse({'ok': 'Register saved!'}, status=201)

    return JsonResponse({'error': 'Cannot find alarm'}, status=404)


def update_alarm(data):
    alarm = Alarm.objects.filter(cup=data['id_cup'], partition=data['partition']).last()

    if alarm:
        start_time = f"{data['alarm_info']['start']['hour']}:{data['alarm_info']['start']['minute']}:00"
        alarm.start_time = start_time

        period = f"{data['alarm_info']['period']['hour']}:{data['alarm_info']['period']['minute']}:00"
        alarm.period = period

        alarm.duration = data['alarm_info']['duration']
        alarm.is_active = True

        alarm.save()
        update_record(data)

        return JsonResponse({'ok': 'Register saved!'}, status=201)
    return JsonResponse({'error': "There's no registered alarms"}, status=404)


def update_record(data):
    alarms = Alarm.objects.filter(cup=data['id_cup'], partition=data['partition'])

    alarm = None
    if alarms:
        alarm = alarms.last()

        try:
            alarm_record = Record.objects.get(alarm=alarm.id)
        except (ObjectDoesNotExist, AttributeError):
            return JsonResponse({'error': 'Cannot find alarm\'s record'}, status=404)

        alarm_record.event = data['event']
        alarm_record.moment = data['moment']
        alarm_record.save()

        return JsonResponse({'ok': 'Register saved!'}, status=201)
    return JsonResponse({'error': "There's no registered alarms"}, status=404)


def alert_contact(data):
    pass
    #  cup = Cup.objects.get(id=data['id_cup'])
    #  contact = cup.contact
    # TODO Send message to contact
