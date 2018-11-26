import json
from datetime import datetime
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

from ..models import User, Cup, Contact, Alarm, Record


@csrf_exempt
def register_info(request):
    try:
        data = json.loads(request.body)
    except ValueError as e:
        return HttpResponse(status=413)

    try:
        cup = Cup.objects.get(pk=data['id_cup'])
    except Exception as e:
        return HttpResponse(status=204)

    # Decides which action to take based on event
    response_code = event_handler(data)
    return HttpResponse(status=response_code, content=request.body)


def event_handler(data):
    if data['event'] == 'registered':
        return register_alarm(data)
    elif data['event'] == 'taken':
        return update_alarm(data)
    elif data['event'] == 'not_taken':
        return alert_contact(data)
    elif data['event'] == 'cancelled':
        return cancel_alarm(data)
    else:
        return 400


def register_alarm(data):
    alarm = Alarm(
        cup=Cup.objects.get(id=data['id_cup']),
        partition=data['partition'],
        start_time=f"{data['alarm_info']['start']['hour']}:{data['alarm_info']['start']['minute']}:00",
        period=f"{data['alarm_info']['period']['hour']}:{data['alarm_info']['period']['minute']}:00",
        duration=data['alarm_info']['duration'],
        is_active=True,
    )
    alarm.save()

    alarm_record = Record(
        alarm=alarm,
        event=data['event'],
        moment=data['moment']
    )
    alarm_record.save()

    return 201


def cancel_alarm(data):
    try:
        alarm = Alarm.objetcs.get(cup=data['id_cup'])
    except:
        return 204
    alarm.is_active = False
    alarm.save()
    update_record(alarm.id, data)

    return 200


def update_alarm(data):
    cup_alarm = Alarm.objects.filter(cup=data['id_cup'], partition=data['partition']).last()

    if not cup_alarm:
        return 204

    start_time = f"{data['alarm_info']['start']['hour']}:{data['alarm_info']['start']['minute']}:00"
    cup_alarm.start_time = start_time

    period = f"{data['alarm_info']['period']['hour']}:{data['alarm_info']['period']['minute']}:00"
    cup_alarm.period = period

    cup_alarm.duration = data['alarm_info']['duration']
    cup_alarm.is_active = True

    cup_alarm.save()
    update_record(cup_alarm.id, data)

    return 200


def update_record(alarm_id, data):
    try:
        alarm_record = Record.objects.get(alarm=alarm_id)
    except:
        return 204
    alarm_record.event = data['event']
    alarm_record.moment = data['moment']
    alarm_record.save()

    return 200


def alert_contact(data):
    cup = Cup.objects.get(id=data['id_cup'])
    contact = cup.contact
    # TODO Send message to contact
