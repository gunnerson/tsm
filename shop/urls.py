from django.urls import path

from . import views

app_name = "shop"

urlpatterns = [
    path('orders/', views.OrderListView.as_view(),
         name='orders'),
    path('orders/create/', views.OrderView.as_view(is_create=True),
         name='create_order'),
    path('orders/<int:pk>/', views.OrderView.as_view(),
         name='order'),
    path('orders/<int:pk>/print', views.OrderPrintView.as_view(),
         name='order_print'),
    path('orders/<int:pk>/budget', views.budget_invoice,
         name='order_budget'),
    path('jobs/', views.JobFormSetView.as_view(),
         name='jobs'),
    path('jobs/<int:pk>/parts/', views.JobPartListView.as_view(),
         name='job_parts'),
    path('jobs/<int:pk>/part_types/', views.JobPartTypeListView.as_view(),
         name='job_part_types'),
    path('part_types/', views.PartTypeFormSetView.as_view(),
         name='part_types'),
    path('parts/', views.PartFormSetView.as_view(),
         name='parts'),
    path('parts/<int:pk>/', views.PartDetailView.as_view(),
         name='part'),
    path('purchases/', views.PurchaseListView.as_view(),
         name='purchases'),
    path('purchases/create/', views.PurchaseView.as_view(is_create=True),
         name='create_purchase'),
    path('purchases/<int:pk>/', views.PurchaseView.as_view(),
         name='purchase'),
    path('purchases/<int:pk>/budget', views.budget_purchase,
         name='purchase_budget'),
    path('accounting/', views.BalanceFormSetView.as_view(),
         name='balance'),
    path('assign/<int:pk>/<slug:unit>/', views.PartPlaceFormSetView.as_view(),
         name='assign_part'),
    path('assign_to_all/<int:pk>/<slug:unit>/', views.assign_to_all,
         name='assign_to_all'),
    path('order_stop/<int:pk>/', views.order_stop,
         name='order_stop'),
    path('shelves/', views.ShelfGroupListView.as_view(),
         name='shelves'),
    path('shelves/add/<int:pk>', views.ShelfCreateView.as_view(),
         name='shelves_add'),
    path('shelves/update/<int:pk>', views.ShelfUpdateView.as_view(),
         name='shelves_update'),
]
