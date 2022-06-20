from typing import Callable

from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest


def get_request(func: Callable[[HttpRequest], HttpResponse]):
    def inner(request: HttpRequest) -> HttpResponse:
        if not request.method == "GET":
            return HttpResponseBadRequest()

        return func(request)

    return inner


def post_request(func: Callable[[HttpRequest], HttpResponse]):
    def inner(request: HttpRequest) -> HttpResponse:
        if not request.method == "POST":
            return HttpResponseBadRequest()

        return func(request)

    return inner