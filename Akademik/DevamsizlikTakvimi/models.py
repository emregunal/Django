from django.db import models
from django.contrib.auth.models import User

class Ders(models.Model):
    ders_kodu = models.CharField(max_length=20, unique=True, verbose_name='Ders Kodu')
    ders_adi = models.CharField(max_length=200, verbose_name='Ders Adı')
    ogretmen = models.CharField(max_length=200, verbose_name='Öğretmen')
    kredi = models.IntegerField(default=3, verbose_name='Kredi')
    haftalik_ders_saati = models.IntegerField(default=3, verbose_name='Haftalık Ders Saati')
    devam_zorunlulugu = models.IntegerField(default=70, verbose_name='Devam Zorunluluğu (%)')
    
    class Meta:
        verbose_name = 'Ders'
        verbose_name_plural = 'Dersler'
    
    def __str__(self):
        return f"{self.ders_kodu} - {self.ders_adi}"
    
    def toplam_ders_saati(self):
        return self.haftalik_ders_saati * 14

class Devamsizlik(models.Model):
    ogrenci = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Öğrenci')
    ders = models.ForeignKey(Ders, on_delete=models.CASCADE, verbose_name='Ders')
    devamsiz_saat = models.IntegerField(default=0, verbose_name='Devamsız Kalınan Saat')
    tarih = models.DateField(auto_now_add=True, verbose_name='Kayıt Tarihi')
    aciklama = models.TextField(blank=True, verbose_name='Açıklama')
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Devamsızlık'
        verbose_name_plural = 'Devamsızlıklar'
        ordering = ['-tarih']
        unique_together = ['ogrenci', 'ders']
    
    def __str__(self):
        return f"{self.ogrenci.username} - {self.ders.ders_adi}"
    
    def devamsizlik_yuzdesi(self):
        toplam_saat = self.ders.toplam_ders_saati()
        if toplam_saat > 0:
            devamsizlik_orani = (self.devamsiz_saat / toplam_saat) * 100
            return round(100 - devamsizlik_orani, 1)
        return 100
    
    def kalan_devamsizlik_hakki(self):
        toplam_saat = self.ders.toplam_ders_saati()
        izin_verilen_devamsizlik = toplam_saat * (100 - self.ders.devam_zorunlulugu) / 100
        return max(0, int(izin_verilen_devamsizlik - self.devamsiz_saat))
