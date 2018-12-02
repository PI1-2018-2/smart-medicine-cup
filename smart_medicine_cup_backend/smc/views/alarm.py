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
        return HttpResponse(status=415, content={'error': 'wrong content-type, use application/json'})

    try:
        data = json.loads(request.body)
        handler = get_event_handler(data['event'])
        response = handler(data)
    except KeyError:
        response = HttpResponse(status=400, content={'error': 'invalid Json'})

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
        return HttpResponse(status=400, content={'error': 'wrong partition range'})

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
        return HttpResponse(status=404, content={'error': 'cannot find cup with given id'})

    alarm_record = Record(
        alarm=alarm,
        event=data['event'],
        moment=data['moment']
    )
    alarm_record.save()

    return HttpResponse(status=201, content={'ok': 'Register saved!'})


def cancel_alarm(data):
    alarm = Alarm.objects.filter(cup=data['id_cup'], partition=data['partition']).last()

    if alarm:
        alarm.is_active = False
        alarm.save()
        update_record(data)
        return HttpResponse(status=201, content={'ok': 'Register saved!'})

    return HttpResponse(status=404, content={'error': 'Cannot find alarm'})


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

        return HttpResponse(status=201, content={'ok': 'Register saved!'})
    return HttpResponse(status=404, content={'error': "There's no registered alarms"})


def update_record(data):
    alarms = Alarm.objects.filter(cup=data['id_cup'], partition=data['partition'])

    alarm = None
    if alarms:
        alarm = alarms.last()

        try:
            alarm_record = Record.objects.get(alarm=alarm.id)
        except (ObjectDoesNotExist, AttributeError):
            return HttpResponse(status=404, content={'error': 'Cannot find alarm\'s record'})

        alarm_record.event = data['event']
        alarm_record.moment = data['moment']
        alarm_record.save()

        return HttpResponse(status=201, content={'ok': 'Register saved!'})
    return HttpResponse(status=404, content={'error': "There's no registered alarms"})


def alert_contact(data):
    pass
    #  cup = Cup.objects.get(id=data['id_cup'])
    #  contact = cup.contact
    # TODO Send message to contact
