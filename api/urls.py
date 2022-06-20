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
from django.urls import path

from api.views import client, transport, payment, check, payment_plane, black_list

urlpatterns = [
    path('clients/', client.all_clients),
    path('client/all', client.all_clients),
    path('client/<int:id>', client.client_by_id),
    path('client/', client.create_client),

    path('transports/', transport.all_transports),
    path('transport/all', transport.all_transports),
    path('transport/<int:id>', transport.transport_by_id),
    path('transport/', transport.create_transport),

    path('payments/', payment.all_payments),
    path('payment/all', payment.all_payments),
    path('payment/<int:id>', payment.payment_by_id),
    path('payment/', payment.create_payment),

    path('payment-planes/', payment_plane.all_payment_pages),
    path('payment-plane/all', payment_plane.all_payment_pages),
    path('payment-plane/<int:id>', payment_plane.payment_plane_by_id),
    path('payment-plane/', payment_plane.create_payment_plane),

    path('checks/', check.all_checks),
    path('check/all', check.all_checks),
    path('check/<int:id>', check.check_by_id),
    path('check/', check.create_check),

    path('black-list/', black_list.all_black_list),
    path('black-list/all', black_list.all_black_list),
    path('black-list/', black_list.create_black_list),
]
