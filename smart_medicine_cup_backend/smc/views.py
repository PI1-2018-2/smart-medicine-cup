import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User, Cup, Partition


@csrf_exempt
def register_info(request):
    print(request.body)
    try:
        data = json.loads(request.body)
    except Exception as e:
        print("============Error: ", e)

    cup = Cup.objects.get(pk=data['id_cup'])
    print(cup)
    partitions = Partition.objects.get(cup=cup)
    print(partitions)
    current_partition = partitions[data['partition']]
    print(current_partition)
    event = data['event']
    print(event)
    if event == 'taken' or event == 'not_taken':
        current_partition.was_taken = event
    elif event == 'registered' or event == 'removed':
        # TODO Create observation attribute
        current_partition.observation = event
    else:
        print("%%%%% Unexpected Event: ", event)

    # Time field
    # current_partition.medicine_time =

    print('dados --->', request.body)
    return HttpResponse(200, {'detail': 'deu bom!'})
