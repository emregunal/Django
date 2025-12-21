from . import views
from django.urls import path


urlpatterns = [
    path('etkinlik-oner/', views.etkinlikOner, name='etkinlik-oner'),
]