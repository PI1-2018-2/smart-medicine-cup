import json
from datetime import datetime
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import User, Cup, Contact, Alarm, Record


@csrf_exempt
def register_info(request):
    print(request.body)
    try:
        data = json.loads(request.body)
    except Exception as e:
        print('Error parsing JSON object: ', e)

    try:
        cup = Cup.objects.get(pk=data['id_cup'])
    except Exception as e:
        print(f'Error: {e}, Cup id not found.')

    # Decides which action to take based on event
    event_handler(data)

    return HttpResponse(200, {'detail': 'deu bom!'})


def event_handler(data):
    if data['event'] == 'registered':
        register_alarm(data)
    elif data['event'] == 'taken':
        update_alarm(data)
    elif data['event'] == 'not_taken':
        alert_contact(data)
    elif data['event'] == 'cancelled':
        cancel_alarm(data)
    else:
        print('[ERROR]: Unhandled event option')


def register_alarm(data):
    alarm = Alarm(
        cup=Cup.objects.get(id=data['id_cup']),
        partition=data['partition'],
        start_time=f"{data['alarm_info']['start']['hour']}:{data['alarm_info']['start']['minute']}:00",
        period=f"{data['alarm_info']['period']['hour']}:{data['alarm_info']['period']['minute']}:00",
        duration=data['alarm_info']['duration'],
        is_active=True,
    )
    print('New alarm registered', alarm)
    alarm.save()

    alarm_record = Record(
        alarm=alarm,
        event=data['event'],
        moment=data['moment']
    )
    print(alarm_record)
    alarm_record.save()


def cancel_alarm(data):
    alarm = Alarm.objetcs.get(cup=data['id_cup'])
    alarm.is_active = False
    alarm.save()
    update_record(alarm.id, data)


def update_alarm(data):
    cup_alarm = Alarm.objects.get(cup=data['id_cup'])
    print('Before', cup_alarm)
    start_time = f"{data['alarm_info']['start']['hour']}:{data['alarm_info']['start']['minute']}:00"
    print(start_time)
    cup_alarm.start_time = start_time

    period = f"{data['alarm_info']['period']['hour']}:{data['alarm_info']['period']['minute']}:00"
    print(period)
    cup_alarm.period = period

    cup_alarm.duration = data['alarm_info']['duration']
    cup_alarm.is_active = True
    print(cup_alarm)

    cup_alarm.save()
    update_record(cup_alarm.id, data)


def update_record(alarm_id, data):
    alarm_record = Record.objects.get(alarm=alarm_id)
    alarm_record.event = data['event']
    alarm_record.moment = data['moment']
    print(alarm_record)
    alarm_record.save()


def alert_contact(data):
    cup = Cup.objects.get(id=data['id_cup'])
    contact = cup.contact
    # TODO Send message to contact
