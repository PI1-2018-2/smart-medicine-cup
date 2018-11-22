import json
from datetime import datetime
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User, Cup, Partition


@csrf_exempt
def register_info(request):
    print(request.body)
    try:
        data = json.loads(request.body)
    except Exception as e:
        print("Error parsing JSON object: ", e)

    cup_id = Cup.objects.get(pk=data['id_cup'])
    print("Cup: ", cup_id)

    partitions = Partition.objects.all().filter(cup_id=cup_id)
    print("Partitions", [p.id for p in partitions])
    print("Selected partition: ", data['partition'])

    current_partition = [p for p in partitions if p.id == data['partition']]
    current_partition = current_partition.pop(0)
    print("Current partition", current_partition)

    if not current_partition:
        print("ERROR: no partition selected")

    event = data['event']
    print("Event: ", event)

    if event == 'taken' or event == 'not_taken':
        current_partition.was_taken = event
    elif event == 'registered' or event == 'removed':
        pass
        # TODO Create observation attribute
        # current_partition.observation = event
    else:
        print("Error: Unexpected Cup Event: ", event)

    print("Partition Event: ", current_partition.was_taken)

    start_time_hour = data["alarm_info"]["start"]["hour"]
    start_time_minute = data["alarm_info"]["start"]["minute"]

    period_time_hour = data["alarm_info"]["period"]["hour"]
    period_time_minute = data["alarm_info"]["period"]["minute"]

    duration = data["alarm_info"]["duration"]

    print(f"start time {start_time_hour}:{start_time_minute}")
    print(f"period time {period_time_hour}:{period_time_minute}")
    print(f"duration time {duration}")

    print('dados --->', request.body)
    return HttpResponse(200, {'detail': 'deu bom!'})
