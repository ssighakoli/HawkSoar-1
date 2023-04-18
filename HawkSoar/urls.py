"""HawkSoar URL Configuration"""



from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include

urlpatterns = [
    path('db_connect/', include('db_connect.urls')),
    path('admin/', admin.site.urls),
]
