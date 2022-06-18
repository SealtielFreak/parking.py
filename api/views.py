import json

from django.core.exceptions import FieldError
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

import api.models


def json_decode(body: bytes, decode: str = "utf-8") -> dict:
    try:
        return json.loads(body.decode(decode))
    except ValueError:
        pass

    return {}


def secure_post(func):
    def inner(self: View, request: HttpRequest):
        try:
            return func(self, request)
        except KeyError:
            raise FieldError("Invalid JSON, contains invalids keys")

    return inner


class StatusResponse:
    def __init__(self):
        self.__data = {
            "status": "unknown",
            "data": {}
        }

    @property
    def json(self) -> JsonResponse:
        return JsonResponse(self.__data)

    @property
    def data(self) -> dict:
        return self.__data["data"]

    def failure(self):
        self.__data["status"] = "failure"

    def success(self):
        self.__data["status"] = "success"


class RequestClients(View):
    CLIENT_KEYS = [
        "id",
        "first_name",
        "last_name",
        "contact_email",
        "rfc",
        "curp",
        "birthday_date",
        "discharge_date",
        "state",
        "suburb",
        "municipality",
        "int_num"
    ]

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        """
        Warning, this method is only for demonstration and debug the api!
        """
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest):
        status = StatusResponse()
        clients = list(api.models.Client.objects.values())
        is_empty = len(clients) == 0

        if not is_empty:
            status.success()
            status.data["number"] = len(clients)
            status.data["clients"] = clients
        else:
            status.failure()

        return status.json

    @secure_post
    def post(self, request: HttpRequest):
        status = StatusResponse()
        data = json_decode(request.body)

        data_client = data["client"]

        if not (data_client.keys() - set(self.CLIENT_KEYS)):
            status.success()
            api.models.Client.objects.create(
                **data["client"]
            )
        else:
            status.data["message"] = "invalid keys"
            status.failure()

        return status.json
