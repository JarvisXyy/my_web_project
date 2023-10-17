from django.urls import path
from . import views

app_name = 'toolbox' #设置命名空间

urlpatterns = [
    path('ip_tools/', views.ip_tools, name='ip_tools'),
    path('port_scan/', views.port_scan_view, name='port_scan'),
]
