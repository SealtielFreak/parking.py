import json

from django.forms import model_to_dict
from django.http import HttpRequest, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt

import api.models


KEYS_FIELDS = {
    field.name for field in api.models.Client._meta.get_fields()
}

def all_list(request: HttpRequest) -> JsonResponse:
    clients = list(api.models.Client.objects.values())

    return JsonResponse({
        "clients": clients
    })


def by_id(request: HttpRequest, id: int) -> JsonResponse:
    client = model_to_dict(api.models.Client.objects.get(id=id))

    return JsonResponse({
        "client": client
    })


# @csrf_exempt
def create(request: HttpRequest) -> JsonResponse:
    return JsonResponse({
        "keys": list(KEYS_FIELDS)
    })
