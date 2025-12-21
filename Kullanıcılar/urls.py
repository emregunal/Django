from django.urls import path
from . import views

app_name = 'kullanicilar'

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profil/', views.profile_view, name='profile'),
    path('api/register/', views.register_api, name='register_api'),
]
