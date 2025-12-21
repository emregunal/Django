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
    # Event management
    admin_events,
    add_event,
    edit_event,
    delete_event,
    approve_event,
    reject_event,
    # Instructor management
    instructor_appointments,
    instructor_approve_appointment,
    instructor_reject_appointment,
    instructor_appointments_table,
    instructor_profile,
    instructor_change_password,
    # Club management
    admin_clubs,
    approve_club,
    reject_club,
    delete_club,
    assign_club_president,
    remove_club_president,
)

urlpatterns = [
    path('login/', admin_login, name='admin_login'),
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('appointments/', admin_appointments, name='admin_appointments'),
    path('approve/<str:appointment_id>/', approve_appointment, name='approve_appointment'),
    path('reject/<str:appointment_id>/', reject_appointment, name='reject_appointment'),
    
    # Event management
    path('events/', admin_events, name='admin_events'),
    path('events/add/', add_event, name='add_event'),
    path('events/edit/<str:event_id>/', edit_event, name='edit_event'),
    path('events/delete/<str:event_id>/', delete_event, name='delete_event'),
    path('events/approve/<str:event_id>/', approve_event, name='approve_event'),
    path('events/reject/<str:event_id>/', reject_event, name='reject_event'),
    
    path('logout/', admin_logout, name='admin_logout'),
    
    # Instructor appointment management
    path('instructor/', instructor_appointments, name='instructor_appointments'),
    path('instructor/approve/<str:appointment_id>/', instructor_approve_appointment, name='instructor_approve_appointment'),
    path('instructor/reject/<str:appointment_id>/', instructor_reject_appointment, name='instructor_reject_appointment'),
    path('instructor/table/', instructor_appointments_table, name='instructor_appointments_table'),
    path('instructor/profile/', instructor_profile, name='instructor_profile'),
    path('instructor/change-password/', instructor_change_password, name='instructor_change_password'),
    
    # Club management
    path('clubs/', admin_clubs, name='admin_clubs'),
    path('clubs/approve/<str:club_id>/', approve_club, name='approve_club'),
    path('clubs/reject/<str:club_id>/', reject_club, name='reject_club'),
    path('clubs/delete/<str:club_id>/', delete_club, name='delete_club'),
    path('clubs/assign-president/', assign_club_president, name='assign_club_president'),
    path('remove-president/', remove_club_president, name='remove_club_president'),
]

