from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def register_info(request):
    print('dados --->', request.body)
    return HttpResponse(200, {'detail': 'deu bom!'})
