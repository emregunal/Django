"""
Admin Panel URLs
"""

from django.urls import path
from Core.admin_views import (
    admin_login,
    admin_dashboard,
    admin_appointments,
    approve_appointment,
    reject_appointment,
    admin_logout,
)

urlpatterns = [
    path('login/', admin_login, name='admin_login'),
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('appointments/', admin_appointments, name='admin_appointments'),
    path('approve/<str:appointment_id>/', approve_appointment, name='approve_appointment'),
    path('reject/<str:appointment_id>/', reject_appointment, name='reject_appointment'),
    path('logout/', admin_logout, name='admin_logout'),
]
