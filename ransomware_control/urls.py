from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ransomware_control.dashboard.urls')),
    path('api/', include('ransomware_control.dashboard.api_urls')),
]