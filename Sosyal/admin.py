from django.contrib import admin
from .models import Etkinlik, Kulup, Duyuru

@admin.register(Etkinlik)
class EtkinlikAdmin(admin.ModelAdmin):
    list_display = ('baslik', 'kategori', 'tarih', 'konum', 'katilimci_sayisi')
    list_filter = ('kategori', 'tarih')
    search_fields = ('baslik', 'konum', 'aciklama')

@admin.register(Kulup)
class KulupAdmin(admin.ModelAdmin):
    list_display = ('ad', 'kategori', 'uye_sayisi')
    list_filter = ('kategori',)
    search_fields = ('ad', 'aciklama')

@admin.register(Duyuru)
class DuyuruAdmin(admin.ModelAdmin):
    list_display = ('baslik', 'kategori', 'goruntulenme', 'olusturma_tarihi')
    list_filter = ('kategori',)
    search_fields = ('baslik', 'icerik')
