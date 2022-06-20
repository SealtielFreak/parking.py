from django.forms import model_to_dict
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET

import api.models
from utilities.decode import json_to_dict

TRANSPORT_FIELDS = {
    field.name for field in api.models.Transport._meta.get_fields()
}


@require_GET
def all_transports(request: HttpRequest) -> HttpResponse:
    data = {}
    transports = list(api.models.Transport.objects.values())

    data["status"] = "success" if transports else "failure"

    if data["status"] == "success":
        data["data"] = transports

    return JsonResponse(data)


@require_GET
def transport_by_id(request: HttpRequest, id: int) -> HttpResponse:
    return JsonResponse({
        "data": model_to_dict(api.models.Transport.objects.get(transport_id=id))
    })


@csrf_exempt
@require_POST
def create_transport(request: HttpRequest) -> HttpResponse:
    transport_data = json_to_dict(request.body)

    if not transport_data:
        return HttpResponseBadRequest()

    api.models.Transport.objects.create(
        **transport_data
    )

    return JsonResponse({
        "status": "success",
        "data": transport_data
    })
