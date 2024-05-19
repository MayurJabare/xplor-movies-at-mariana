from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('movies/',include('app.urls')),
    path('api/',include('api.urls'))
]
