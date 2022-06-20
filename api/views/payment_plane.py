from django.forms import model_to_dict
from django.http import HttpRequest, JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

import api.models
from utilities.decode import json_to_dict

PAYMENT_PLANE_FIELDS = {
    field.name for field in api.models.PaymentPlane._meta.get_fields()
}


@require_GET
def all_payment_pages(request: HttpRequest) -> HttpResponse:
    data = {}
    payments = list(api.models.PaymentPlane.objects.values())

    data["status"] = "success" if payments else "failure"

    if data["status"] == "success":
        data["data"] = payments

    return JsonResponse(data)


@require_GET
def payment_plane_by_id(request: HttpRequest, id: int) -> HttpResponse:
    return JsonResponse({
        "data": model_to_dict(api.models.PaymentPlane.objects.get(payment_id=id))
    })


@csrf_exempt
@require_POST
def create_payment_plane(request: HttpRequest) -> HttpResponse:
    check_data = json_to_dict(request.body)

    if check_data:
        return HttpResponseBadRequest()

    api.models.PaymentPlane.objects.create(
        **check_data
    )

    return JsonResponse({
        "status": "success",
        "data": check_data
    })
