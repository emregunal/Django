from django.contrib import admin
from .models import Ogretmen, Randevu

@admin.register(Ogretmen)
class OgretmenAdmin(admin.ModelAdmin):
    list_display = ['kullanici', 'unvan', 'bolum', 'ofis']
    search_fields = ['kullanici__username', 'kullanici__first_name', 'kullanici__last_name', 'bolum']

@admin.register(Randevu)
class RandevuAdmin(admin.ModelAdmin):
    list_display = ['ogrenci', 'ogretmen', 'tarih', 'baslangic_saati', 'durum']
    list_filter = ['durum', 'tarih']
    search_fields = ['ogrenci__username', 'ogretmen__kullanici__username', 'konu']
    date_hierarchy = 'tarih'
