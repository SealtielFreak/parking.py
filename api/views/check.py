from django.forms import model_to_dict
from django.http import HttpRequest, JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

import api.models
from utilities.decode import json_to_dict

CHECK_FIELDS = {
    field.name for field in api.models.Check._meta.get_fields()
}


@require_GET
def all_checks(request: HttpRequest) -> HttpResponse:
    data = {}
    checks = list(api.models.Check.objects.values())

    data["status"] = "success" if checks else "failure"

    if data["status"] == "success":
        data["data"] = checks

    return JsonResponse(data)


@require_GET
def check_by_id(request: HttpRequest, id: int) -> HttpResponse:
    return JsonResponse({
        "data": model_to_dict(api.models.Check.objects.get(check_id=id))
    })


@csrf_exempt
@require_POST
def create_check(request: HttpRequest) -> HttpResponse:
    check_data = json_to_dict(request.body)

    if check_data:
        return HttpResponseBadRequest()

    api.models.Check.objects.create(
        **check_data
    )

    return JsonResponse({
        "status": "success",
        "data": check_data
    })
