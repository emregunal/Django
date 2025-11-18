from django.db import models
from django.contrib.auth.models import User

class Ogretmen(models.Model):
    kullanici = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Kullanıcı')
    unvan = models.CharField(max_length=100, verbose_name='Ünvan')
    bolum = models.CharField(max_length=200, verbose_name='Bölüm')
    ofis = models.CharField(max_length=100, verbose_name='Ofis', blank=True)
    telefon = models.CharField(max_length=20, verbose_name='Telefon', blank=True)
    
    class Meta:
        verbose_name = 'Öğretmen'
        verbose_name_plural = 'Öğretmenler'
    
    def __str__(self):
        return f"{self.unvan} {self.kullanici.get_full_name()}"

class Randevu(models.Model):
    DURUM_SECENEKLERI = [
        ('bekliyor', 'Onay Bekliyor'),
        ('onaylandi', 'Onaylandı'),
        ('reddedildi', 'Reddedildi'),
        ('tamamlandi', 'Tamamlandı'),
        ('iptal', 'İptal Edildi'),
    ]
    
    ogrenci = models.ForeignKey(User, on_delete=models.CASCADE, related_name='randevular', verbose_name='Öğrenci')
    ogretmen = models.ForeignKey(Ogretmen, on_delete=models.CASCADE, verbose_name='Öğretmen')
    tarih = models.DateField(verbose_name='Tarih')
    baslangic_saati = models.TimeField(verbose_name='Başlangıç Saati')
    bitis_saati = models.TimeField(verbose_name='Bitiş Saati')
    konu = models.CharField(max_length=200, verbose_name='Konu')
    aciklama = models.TextField(verbose_name='Açıklama', blank=True)
    durum = models.CharField(max_length=20, choices=DURUM_SECENEKLERI, default='bekliyor', verbose_name='Durum')
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)
    guncelleme_tarihi = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Randevu'
        verbose_name_plural = 'Randevular'
        ordering = ['-tarih', '-baslangic_saati']
    
    def __str__(self):
        return f"{self.ogrenci.username} - {self.ogretmen} - {self.tarih}"
