from django.urls import path

from .views import (
    OrderListView,
    OrderCreateView,
    OrderUpdateView,
)

app_name = "shop"

urlpatterns = [
    path('orders/', OrderListView.as_view(),
         name='orders'),
    path('orders/create', OrderCreateView.as_view(),
         name='create_order'),
    path('orders/<int:pk>', OrderUpdateView.as_view(),
         name='order'),
]
