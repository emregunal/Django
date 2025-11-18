from . import views
from django.urls import path


urlpatterns = [
    path('canli-akademik-takvim/', views.canliAkademikTakvim, name='canli-akademik-takvim'),
]