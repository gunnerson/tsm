from django.urls import path

from .views import (
    OrderListView,
    OrderView,
    JobFormSetView,
    JobPartsSetView,
)

app_name = "shop"

urlpatterns = [
    path('orders/', OrderListView.as_view(),
         name='orders'),
    path('orders/create', OrderView.as_view(is_create=True),
         name='create_order'),
    path('orders/<int:pk>', OrderView.as_view(),
         name='order'),
    path('jobs/', JobFormSetView.as_view(),
         name='jobs'),
    path('jobs/<int:pk>/parts', JobPartsSetView.as_view(),
         name='job_parts'),
]
