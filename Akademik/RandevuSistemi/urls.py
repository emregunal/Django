from . import views
from django.urls import path


urlpatterns = [
    path('randevu-sistemi/', views.randevuSistemi, name='randevu-sistemi'),
]