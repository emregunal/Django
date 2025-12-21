from django.contrib import admin
from .models import Etkinlik, Kulup, Duyuru

@admin.register(Etkinlik)
class EtkinlikAdmin(admin.ModelAdmin):
    list_display = ['baslik', 'kategori', 'tarih', 'konum', 'katilimci_sayisi', 'olusturan']
    list_filter = ['kategori', 'tarih']
    search_fields = ['baslik', 'aciklama', 'konum']
    date_hierarchy = 'tarih'
    filter_horizontal = ['katilimcilar']

@admin.register(Kulup)
class KulupAdmin(admin.ModelAdmin):
    list_display = ['ad', 'kategori', 'uye_sayisi', 'kurucu']
    list_filter = ['kategori']
    search_fields = ['ad', 'aciklama']
    filter_horizontal = ['uyeler']

@admin.register(Duyuru)
class DuyuruAdmin(admin.ModelAdmin):
    list_display = ['baslik', 'kategori', 'yazar', 'olusturma_tarihi', 'goruntulenme']
    list_filter = ['kategori', 'olusturma_tarihi']
    search_fields = ['baslik', 'icerik']
    date_hierarchy = 'olusturma_tarihi'
