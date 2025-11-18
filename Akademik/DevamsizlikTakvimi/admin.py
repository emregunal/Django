from django.contrib import admin
from .models import Ders, Devamsizlik

@admin.register(Ders)
class DersAdmin(admin.ModelAdmin):
    list_display = ['ders_kodu', 'ders_adi', 'ogretmen', 'haftalik_ders_saati', 'devam_zorunlulugu']
    search_fields = ['ders_kodu', 'ders_adi', 'ogretmen']

@admin.register(Devamsizlik)
class DevamsizlikAdmin(admin.ModelAdmin):
    list_display = ['ogrenci', 'ders', 'devamsiz_saat', 'devamsizlik_yuzdesi', 'tarih']
    list_filter = ['tarih', 'ders']
    search_fields = ['ogrenci__username', 'ders__ders_adi']
    date_hierarchy = 'tarih'
