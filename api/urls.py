"""parking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

import api.views as views
from api.views import client, transport


urlpatterns = [
    path('payments', csrf_exempt(views.RequestPayment.as_view()), name="payments"),
    path('transports', csrf_exempt(views.RequestTransports.as_view()), name="transports"),
    path('pages', csrf_exempt(views.RequestPages.as_view()), name="pages"),
    path('black-list', csrf_exempt(views.RequestBlackList.as_view()), name="black-list"),

    path('clients', client.all_clients),
    path('client/all', client.all_clients),
    path('client/<int:id>',client.client_by_id),
    path('client', client.create_client),

    path('transports/', transport.all_transports),
    path('transports/all', transport.all_transports),
    path('transports/<int:id>', transport.transport_by_id),
]
