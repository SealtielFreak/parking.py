import json

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, JsonResponse
from django.views import View

import api.models


class RequestClients(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest):
        clients = list(api.models.Client.objects.values())

        return JsonResponse({"message": "Success", "clients": f"{clients}"} if not len(clients) == 0 else { "message": "Failure" } )

    def post(self, request: HttpRequest):
        data = request.body

        return JsonResponse({ "message": "Success", "body": data})