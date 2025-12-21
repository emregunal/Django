"""
URL configuration for DoEvent project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    # Django varsayılan admin paneli devre dışı - özel admin panel kullanılıyor
    # path('admin/', admin.site.urls),
    path('admin-panel/', include('Core.admin_urls')),  # Custom admin panel
    path('', include('Core.urls')),  # Ana sayfa
    path('Kullanıcılar/', include('Kullanıcılar.urls')),
    path('Akademik/', include('Akademik.urls')),
    path('Akademik/', include('Akademik.AkademikTakvim.urls')),
    path('Akademik/', include('Akademik.DevamsizlikTakvimi.urls')),
    path('Akademik/', include('Akademik.RandevuSistemi.urls')),
    path('Sosyal/', include('Sosyal.urls')),
    path('Sosyal/', include('Sosyal.Etkinlik.urls')),
    path('Sosyal/', include('Sosyal.EtkinlikOner.urls')),
    path('Sosyal/', include('Sosyal.Kulup.urls')),
    path('Sosyal/', include('Sosyal.KulupOner.urls')),
    
]