from django.forms import model_to_dict
from django.http import HttpRequest, JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

import api.models
from utilities.decode import json_to_dict

CLIENT_FIELDS = {
    field.name for field in api.models.Client._meta.get_fields()
}


@require_GET
def all_clients(request: HttpRequest) -> HttpResponse:
    data = {}
    clients = list(api.models.Client.objects.values())

    return JsonResponse({
        "data": clients
    })

    if data["status"] == "success":
        data["data"] = clients

    return JsonResponse(data)


@require_GET
def client_by_id(request: HttpRequest, id: int) -> HttpResponse:
    return JsonResponse({
        "data": model_to_dict(api.models.Client.objects.get(client_id=id))
    })

@csrf_exempt
@require_POST
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
