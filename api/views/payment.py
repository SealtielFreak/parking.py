from django.forms import model_to_dict
from django.http import HttpRequest, JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

import api.models
from utilities.decode import json_to_dict

PAYMENT_FIELDS = {
    field.name for field in api.models.Payment._meta.get_fields()
}


@require_GET
def all_payments(request: HttpRequest) -> HttpResponse:
    data = {}
    payments = list(api.models.Payment.objects.values())

    data["status"] = "success" if payments else "failure"

    if data["status"] == "success":
        data["data"] = payments

    return JsonResponse(data)


@require_GET
def payment_by_id(request: HttpRequest, id: int) -> HttpResponse:
    return JsonResponse({
        "data": model_to_dict(api.models.Payment.objects.get(payment_id=id))
    })


@csrf_exempt
@require_POST
def create_payment(request: HttpRequest) -> HttpResponse:
    check_data = json_to_dict(request.body)

    if check_data:
        return HttpResponseBadRequest()

    api.models.Payment.objects.create(
        **check_data
    )

    return JsonResponse({
        "status": "success",
        "data": check_data
    })
