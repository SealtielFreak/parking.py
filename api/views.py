import json

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, JsonResponse
from django.views import View

import api.models


class RequestClients(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        """
        Warning!
        """
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest):
        data = {}
        clients = list(api.models.Client.objects.values())
        is_empty = len(clients) == 0

        if not is_empty:
            data["message"] = "success"
        else:
            data["message"] = "failure"

        return JsonResponse(data)

    def post(self, request: HttpRequest):
        data = request.body

        return JsonResponse({ "message": "Success", "body": data})