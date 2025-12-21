from . import views
from django.urls import path


urlpatterns = [
    path('etkinlikler/', views.etkinlikler, name='etkinlikler'),
    path('kulupler/', views.kulupler, name='kulupler'),
    path('duyurular/', views.duyurular, name='duyurular'),
    path('etkinlik/<str:etkinlik_id>/katil/', views.etkinlik_katil, name='etkinlik-katil'),
    path('kulup/<str:kulup_id>/katil/', views.kulup_katil, name='kulup-katil'),
]