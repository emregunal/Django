from . import views
from django.urls import path


urlpatterns = [
    path('etkinlik/<int:id>/', views.etkinlik, name='etkinlik-detay'),
]