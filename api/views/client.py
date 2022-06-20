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

    return JsonResponse({
        "data": clients
    })

    if data["status"] == "success":
        data["data"] = clients

    return JsonResponse(data)


@get_request
def client_by_id(request: HttpRequest, id: int) -> HttpResponse:
    return JsonResponse({
        "data": model_to_dict(api.models.Client.objects.get(client_id=id))
    })

@csrf_exempt
@post_request
def create_client(request: HttpRequest) -> HttpResponse:
    client_data = json_to_dict(request.body)
    print(client_data["data"])
    if not client_data["data"]:
        return HttpResponseBadRequest({
            "status":"400",
            "error" : True,
            "message" : "Error en los parametros enviados!"
        })
        
    # print(CLIENT_FIELDS)
    # if CLIENT_FIELDS - client_data.keys():
    #     print("sin todos los campos")
    #     return HttpResponseBadRequest()

    api.models.Client.objects.create(
        **client_data["data"]
    )

    return JsonResponse({
        "status": "200",
        "message" : "Cliente creado con exito!"
    })
