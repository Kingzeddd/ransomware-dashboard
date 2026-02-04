"""
URLs pour le dashboard
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('machine/<str:machine_id>/', views.machine_detail, name='machine_detail'),
    path('machine/<str:machine_id>/activate/', views.activate_machine, name='activate_machine'),
    path('machine/<str:machine_id>/decrypt/', views.decrypt_machine, name='decrypt_machine'),
    path('machine/<str:machine_id>/payment/', views.mark_payment, name='mark_payment'),
    path('machine/<str:machine_id>/delete/', views.delete_machine, name='delete_machine'),
]
