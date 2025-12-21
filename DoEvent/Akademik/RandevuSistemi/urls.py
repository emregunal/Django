from . import views
from django.urls import path


urlpatterns = [
    path('randevu-sistemi/', views.randevuSistemi, name='randevu-sistemi'),
    path('randevu-yonetim/', views.randevuYonetim, name='randevu-yonetim'),
]