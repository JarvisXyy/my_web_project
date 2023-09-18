from django.urls import path
from . import views

urlpatterns = [
    path('ip_tools/', views.ip_tools, name='ip_tools')
]
