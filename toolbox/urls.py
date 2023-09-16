from django.urls import path
from . import views

urlpatterns = [
    path('ip_address/', views.ip_address, name='ip_address'),
    path('dns_lookup/', views.dns_lookup, name='dns_lookup'),
]
