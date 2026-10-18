from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("stock/", views.stock_list, name="stock_list"),
    path("resellers/", views.reseller_list, name="reseller_list"),
    path("reseller/<int:pk>/", views.reseller_detail, name="reseller_detail"),
    path("map/", views.distribution_map, name="distribution_map"),
    path("inventory/", views.inventory_command_center, name="inventory"),
    path("webhook/<str:token>/", views.telegram_webhook, name="telegram_webhook"),
]