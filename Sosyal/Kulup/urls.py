from . import views
from django.urls import path

urlpatterns = [
    path('kulup/<int:id>/', views.kulup, name='kulup-detay'),
]