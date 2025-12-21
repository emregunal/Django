from django.db import models
from django.contrib.auth.models import User

class AkademikEtkinlik(models.Model):
    ETKINLIK_TIPLERI = [
        ('sinav', 'Sınav'),
        ('odev', 'Ödev Teslim'),
        ('proje', 'Proje Sunumu'),
        ('tatil', 'Tatil'),
        ('diger', 'Diğer'),
    ]
    
    baslik = models.CharField(max_length=200, verbose_name='Başlık')
    aciklama = models.TextField(verbose_name='Açıklama')
    tarih = models.DateField(verbose_name='Tarih')
    baslangic_saati = models.TimeField(verbose_name='Başlangıç Saati', null=True, blank=True)
    bitis_saati = models.TimeField(verbose_name='Bitiş Saati', null=True, blank=True)
    tip = models.CharField(max_length=20, choices=ETKINLIK_TIPLERI, default='diger', verbose_name='Etkinlik Tipi')
    konum = models.CharField(max_length=200, verbose_name='Konum', blank=True)
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Akademik Etkinlik'
        verbose_name_plural = 'Akademik Etkinlikler'
        ordering = ['tarih', 'baslangic_saati']
    
    def __str__(self):
        return f"{self.baslik} - {self.tarih}"
