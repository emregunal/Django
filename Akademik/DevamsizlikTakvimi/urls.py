from . import views
from django.urls import path


urlpatterns = [
    path('devamsizlik-takvimi/', views.devamsizlikTakvimi, name='devamsizlik-takvimi'),
]