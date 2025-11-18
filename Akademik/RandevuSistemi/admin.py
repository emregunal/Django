from django.contrib import admin
from .models import Ogretmen, Randevu

@admin.register(Ogretmen)
class OgretmenAdmin(admin.ModelAdmin):
    list_display = ['kullanici', 'unvan', 'bolum', 'ofis']
    search_fields = ['kullanici__username', 'kullanici__first_name', 'kullanici__last_name', 'bolum']

@admin.register(Randevu)
class RandevuAdmin(admin.ModelAdmin):
    list_display = ['ogrenci', 'ogretmen', 'tarih', 'baslangic_saati', 'durum', 'konu']
    list_filter = ['durum', 'tarih', 'ogretmen']
    search_fields = ['ogrenci__username', 'ogretmen__kullanici__username', 'konu']
    date_hierarchy = 'tarih'
    actions = ['onayla', 'reddet']
    readonly_fields = ['olusturma_tarihi', 'guncelleme_tarihi']
    
    def onayla(self, request, queryset):
        updated = queryset.update(durum='onaylandi')
        self.message_user(request, f'{updated} randevu onaylandı.')
    onayla.short_description = '✅ Seçili randevuları onayla'
    
    def reddet(self, request, queryset):
        updated = queryset.update(durum='reddedildi')
        self.message_user(request, f'{updated} randevu reddedildi.')
    reddet.short_description = '❌ Seçili randevuları reddet'
