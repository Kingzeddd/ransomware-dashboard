"""
Admin configuration pour le dashboard
"""

from django.contrib import admin
from .models import InfectedMachine, StatusLog

@admin.register(InfectedMachine)
class InfectedMachineAdmin(admin.ModelAdmin):
    list_display = ('machine_id', 'hostname', 'username', 'is_activated', 'is_encrypted', 'payment_received', 'registered_at')
    list_filter = ('is_activated', 'is_encrypted', 'payment_received')
    search_fields = ('machine_id', 'hostname', 'username')
    readonly_fields = ('registered_at', 'activated_at', 'encrypted_at', 'decrypted_at', 'last_seen')

@admin.register(StatusLog)
class StatusLogAdmin(admin.ModelAdmin):
    list_display = ('machine', 'status', 'timestamp')
    list_filter = ('status', 'timestamp')
    search_fields = ('machine__hostname', 'status', 'details')
    readonly_fields = ('timestamp',)
