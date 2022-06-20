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

        client = data["client"]

        if not (client.keys() - set(self.CLIENT_KEYS)):
            status.success()
            api.models.Client.objects.create(
                client
            )
        else:
            status.data["message"] = "invalid keys"
            status.failure()

        return status.json


class RequestPayment(View):
    KEYS = [
        "hours",
        "mobility"
    ]

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        """
        Warning, this method is only for demonstration and debug the api!
        """
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest):
        status = StatusResponse()
        payments = list(api.models.PaymentPlane.objects.values())
        is_empty = len(payments) == 0

        if not is_empty:
            status.success()
            status.data["number"] = len(payments)
            status.data["payments"] = payments
        else:
            status.failure()

        return status.json

    @secure_post
    def post(self, request: HttpRequest):
        status = StatusResponse()
        data = json_decode(request.body)

        payment = data["payment"]

        if not (payment.keys() - set(self.KEYS)):
            status.success()
            api.models.PaymentPlane.objects.create(
                **payment
            )
        else:
            status.data["message"] = "invalid keys"
            status.failure()

        return status.json


class RequestTransports(View):
    KEYS = [
        "id_client",
        "id_payment",
        "circulation_card",
        "model",
        "brand",
        "license",
        "type",
        "time_init",
        "time_final"
    ]

    def get(self, request: HttpRequest):
        status = StatusResponse()
        transport = list(api.models.Transport.objects.values())
        is_empty = len(transport) == 0

        if not is_empty:
            status.success()
            status.data["number"] = len(transport)
            status.data["transport"] = transport
        else:
            status.failure()

        return status.json

    @secure_post
    def post(self, request: HttpRequest):
        status = StatusResponse()
        data = json_decode(request.body)

        transport = data["transport"]

        if not (transport.keys() - set(self.KEYS)):
            status.success()
            api.models.Transport.objects.create(
                **transport
            )
        else:
            status.data["message"] = "invalid keys"
            status.failure()

        return status.json


class RequestPages(View):
    KEYS = [
        "id_transport",
        "total",
        "type",
        "date_page"
    ]

    def get(self, request: HttpRequest):
        status = StatusResponse()
        pages = list(api.models.Payment.objects.values())
        is_empty = len(pages) == 0

        if not is_empty:
            status.success()
            status.data["number"] = len(pages)
            status.data["pages"] = pages
        else:
            status.failure()

        return status.json

    @secure_post
    def post(self, request: HttpRequest):
        status = StatusResponse()
        data = json_decode(request.body)

        pages = data["page"]

        if not (pages.keys() - set(self.KEYS)):
            status.success()
            api.models.Payment.objects.create(
                **pages
            )
        else:
            status.data["message"] = "invalid keys"
            status.failure()

        return status.json


class RequestBlackList(View):
    KEYS = [
        "id_client",
    ]

    def get(self, request: HttpRequest):
        status = StatusResponse()
        black_list = list(api.models.BlackList.objects.values())
        is_empty = len(black_list) == 0

        if not is_empty:
            status.success()
            status.data["number"] = len(black_list)
            status.data["black-list"] = black_list
        else:
            status.failure()

        return status.json

    @secure_post
    def post(self, request: HttpRequest):
        status = StatusResponse()
        data = json_decode(request.body)

        black_list = data["black-list"]

        if not (black_list.keys() - set(self.KEYS)):
            status.success()
            api.models.BlackList.objects.create(
                **black_list
            )
        else:
            status.data["message"] = "invalid keys"
            status.failure()

        return status.json
