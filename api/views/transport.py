from django.forms import model_to_dict
from django.http import HttpRequest, HttpResponse, JsonResponse

import api.models
from utilities.request import get_request

TRANSPORT_FIELDS = {
    field.name for field in api.models.Client._meta.get_fields()
}


@get_request
def all_transports(request: HttpRequest) -> HttpResponse:
    data = {}
    transports = list(api.models.Transport.objects.values())

    data["status"] = "success" if transports else "failure"

    if data["status"] == "sucess":
        data["clients"] = transports

    return JsonResponse(data)


@get_request
def transport_by_id(request: HttpRequest, id: int) -> HttpResponse:
    transports = model_to_dict(api.models.Transport.objects.get(client_id=id))