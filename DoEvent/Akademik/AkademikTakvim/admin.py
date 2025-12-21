from django.contrib import admin
from .models import AkademikEtkinlik

@admin.register(AkademikEtkinlik)
class AkademikEtkinlikAdmin(admin.ModelAdmin):
    list_display = ['baslik', 'tarih', 'tip', 'konum', 'olusturma_tarihi']
    list_filter = ['tip', 'tarih']
    search_fields = ['baslik', 'aciklama', 'konum']
    date_hierarchy = 'tarih'
