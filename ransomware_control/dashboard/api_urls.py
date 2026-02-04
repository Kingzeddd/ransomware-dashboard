"""
URLs pour les API
"""

from django.urls import path
from . import api_views

urlpatterns = [
    path('register', api_views.register_machine, name='api_register'),
    path('check_activation/<str:machine_id>', api_views.check_activation, name='api_check_activation'),
    path('save_key', api_views.save_encryption_key, name='api_save_key'),
    path('get_key/<str:machine_id>', api_views.get_encryption_key, name='api_get_key'),
    path('status', api_views.update_status, name='api_status'),
]
