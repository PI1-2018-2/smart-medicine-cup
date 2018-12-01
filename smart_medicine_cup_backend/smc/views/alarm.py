import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

from ..models import User, Cup, Contact, Alarm, Record


@csrf_exempt
def register_info(request):
    if request.method != 'POST':
        return HttpResponse(status=405, content={'error': 'wrong method, use POST'})

    if request.content_type != 'application/json':
        print(request.content_type)
        return HttpResponse(status=415, content={'error': 'wrong content-type, use application/json'})

    try:
        data = json.loads(request.body)
    except ValueError:
        return HttpResponse(status=400, content={'error': 'wrong JSON format'})

    try:
        Cup.objects.get(pk=data['id_cup'])
    except ObjectDoesNotExist:
        return HttpResponse(status=404, content={'error': 'cannot find cup id'})

    # Decides which action to take based on event
    return event_handler(data)


def event_handler(data):
    if data['event'] == 'registered':
        return register_alarm(data)
    if data['event'] == 'taken':
        return update_record(data)
    if data['event'] == 'not_taken':
        return alert_contact(data)
    if data['event'] == 'cancelled':
        return cancel_alarm(data)

    return HttpResponse(status=400, content={'error': 'cannot handle event'})


def register_alarm(data):
    if data['partition'] > 4 or data['partition'] < 1:
        return HttpResponse(status=400, content={'error': 'wrong partition range'})

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

    return HttpResponse(status=201)


def cancel_alarm(data):
    try:
        alarm = Alarm.objects.filter(cup=data['id_cup'], partition=data['partition']).last()
    except ObjectDoesNotExist:
        return HttpResponse(status=404, content={'error': 'Cannot find alarm'})

    if alarm:
        alarm.is_active = False
        alarm.save()
        update_record(data)
        return HttpResponse(status=201)

    return HttpResponse(status=404, content={'error': 'Cannot find alarm'})


def update_alarm(data):
    alarm = Alarm.objects.filter(cup=data['id_cup'], partition=data['partition']).last()

    if not alarm:
        return HttpResponse(status=404, content={'error': 'Cannot find alarm'})

    start_time = f"{data['alarm_info']['start']['hour']}:{data['alarm_info']['start']['minute']}:00"
    alarm.start_time = start_time

    period = f"{data['alarm_info']['period']['hour']}:{data['alarm_info']['period']['minute']}:00"
    alarm.period = period

    alarm.duration = data['alarm_info']['duration']
    alarm.is_active = True

    alarm.save()
    update_record(data)

    return HttpResponse(status=201)


def update_record(data):
    try:
        alarm = Alarm.objects.filter(cup=data['id_cup'], partition=data['partition']).last()
    except ObjectDoesNotExist:
        return HttpResponse(status=404, content={'error': 'Cannot find alarm'})

    try:
        alarm_record = Record.objects.get(alarm=alarm.id)
    except (ObjectDoesNotExist, AttributeError):
        return HttpResponse(status=404, content={'error': 'Cannot find alarm\'s record'})

    alarm_record.event = data['event']
    alarm_record.moment = data['moment']
    alarm_record.save()

    return HttpResponse(status=201)


def alert_contact(data):
    pass
    #  cup = Cup.objects.get(id=data['id_cup'])
    #  contact = cup.contact
    # TODO Send message to contact
