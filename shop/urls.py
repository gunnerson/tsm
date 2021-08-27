from django.urls import path

from .views import (
    OrderListView,
    OrderCreateView,
    OrderDetailView,
    OrderUpdateView,
)

app_name = "shop"

urlpatterns = [
    path('orders/', OrderListView.as_view(),
         name='orders'),
    path('orders/create', OrderCreateView.as_view(),
         name='create_order'),
    path('order/<int:pk>', OrderDetailView.as_view(),
         name='order'),
    path('order/<int:pk>/update', OrderUpdateView.as_view(),
         name='update_order'),
]
