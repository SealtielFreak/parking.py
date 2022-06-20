from django.forms import model_to_dict
from django.http import HttpRequest, JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

import api.models
from utilities.decode import json_to_dict

BLACK_LIST_FIELDS = {
    field.name for field in api.models.BlackList._meta.get_fields()
}


@require_GET
def all_black_list(request: HttpRequest) -> HttpResponse:
    data = {}
    payments = list(api.models.BlackList.objects.values())

    data["status"] = "success" if payments else "failure"

    if data["status"] == "success":
        data["data"] = payments

    return JsonResponse(data)


@require_GET
def black_list_by_id(request: HttpRequest, id: int) -> HttpResponse:
    return JsonResponse({
        "data": model_to_dict(api.models.BlackList.objects.get(payment_id=id))
    })


@csrf_exempt
@require_POST
def create_black_list(request: HttpRequest) -> HttpResponse:
    check_data = json_to_dict(request.body)

    if check_data:
        return HttpResponseBadRequest()

    api.models.BlackList.objects.create(
        **check_data
    )

    return JsonResponse({
        "status": "success",
        "data": check_data
    })
