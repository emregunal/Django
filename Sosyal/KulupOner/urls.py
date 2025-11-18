from . import views
from django.urls import path


urlpatterns = [
    path('kulup-oner/', views.kulupOner, name='kulup-oner'),
]