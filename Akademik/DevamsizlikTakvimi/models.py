from django.db import models
from django.contrib.auth.models import User

class Ders(models.Model):
    ders_kodu = models.CharField(max_length=20, unique=True, verbose_name='Ders Kodu')
    ders_adi = models.CharField(max_length=200, verbose_name='Ders Adı')
    ogretmen = models.CharField(max_length=200, verbose_name='Öğretmen')
    kredi = models.IntegerField(default=3, verbose_name='Kredi')
    
    class Meta:
        verbose_name = 'Ders'
        verbose_name_plural = 'Dersler'
    
    def __str__(self):
        return f"{self.ders_kodu} - {self.ders_adi}"

class Devamsizlik(models.Model):
    ogrenci = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Öğrenci')
    ders = models.ForeignKey(Ders, on_delete=models.CASCADE, verbose_name='Ders')
    tarih = models.DateField(verbose_name='Tarih')
    mazeret = models.BooleanField(default=False, verbose_name='Mazeretli')
    aciklama = models.TextField(blank=True, verbose_name='Açıklama')
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Devamsızlık'
        verbose_name_plural = 'Devamsızlıklar'
        ordering = ['-tarih']
    
    def __str__(self):
        return f"{self.ogrenci.username} - {self.ders.ders_adi} - {self.tarih}"
