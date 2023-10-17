from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('home_page/',views.home_page_view,name='home_page')
]