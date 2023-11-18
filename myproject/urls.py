
from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('toolbox/', include('toolbox.urls')),
    path('news/',include('news.urls')),
    path('',include('core.urls'))

]
