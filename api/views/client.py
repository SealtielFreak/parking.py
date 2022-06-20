from django.forms import model_to_dict
from django.http import HttpRequest, JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt

import api.models
from utilities.decode import json_to_dict
from utilities.request import post_request, get_request

CLIENT_FIELDS = {
    field.name for field in api.models.Client._meta.get_fields()
}


@get_request
def all_clients(request: HttpRequest) -> HttpResponse:
    data = {}
    clients = list(api.models.Client.objects.values())

    data["status"] = "success" if clients else "failure"

    if data["status"] == "success":
        data["clients"] = clients

    return JsonResponse(data)


@get_request
def client_by_id(request: HttpRequest, id: int) -> HttpResponse:
    client = model_to_dict(api.models.Client.objects.get(client_id=id))

    return JsonResponse({
        "client": client
    })


@csrf_exempt
@post_request
def create_client(request: HttpRequest) -> HttpResponse:
    client_data = json_to_dict(request.body)

    if client_data:
        return HttpResponseBadRequest()

    api.models.Client.objects.create(
        **client_data
    )

    return JsonResponse({
        "status": "success",
        "client": client_data
    })
