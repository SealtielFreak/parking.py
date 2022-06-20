from django.forms import model_to_dict
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

import api.models
from utilities.decode import json_to_dict
from utilities.request import get_request, post_request

TRANSPORT_FIELDS = {
    field.name for field in api.models.Transport._meta.get_fields()
}


@get_request
def all_transports(request: HttpRequest) -> HttpResponse:
    data = {}
    transports = list(api.models.Transport.objects.values())

    data["status"] = "success" if transports else "failure"

    if data["status"] == "success":
        data["data"] = transports

    return JsonResponse(data)


@get_request
def transport_by_id(request: HttpRequest, id: int) -> HttpResponse:
    return JsonResponse({
        "data": model_to_dict(api.models.Client.objects.get(client_id=id))
    })


@csrf_exempt
@post_request
def create_transport(request: HttpRequest) -> HttpResponse:
    transport_data = json_to_dict(request.body)

    if transport_data:
        return HttpResponseBadRequest()

    api.models.Transport.objects.create(
        **transport_data
    )

    return JsonResponse({
        "status": "success",
        "data": transport_data
    })
