from django.db import models
from django.contrib.auth.models import User

class Etkinlik(models.Model):
    KATEGORI_SECENEKLERI = [
        ('konser', 'Konser'),
        ('konferans', 'Konferans'),
        ('spor', 'Spor'),
        ('sosyal', 'Sosyal'),
        ('akademik', 'Akademik'),
        ('tiyatro', 'Tiyatro'),
    ]
    
    baslik = models.CharField(max_length=200, verbose_name='Başlık')
    aciklama = models.TextField(verbose_name='Açıklama')
    kategori = models.CharField(max_length=20, choices=KATEGORI_SECENEKLERI, verbose_name='Kategori')
    tarih = models.DateField(verbose_name='Tarih')
    baslangic_saati = models.TimeField(verbose_name='Başlangıç Saati')
    bitis_saati = models.TimeField(verbose_name='Bitiş Saati')
    konum = models.CharField(max_length=200, verbose_name='Konum')
    katilimcilar = models.ManyToManyField(User, related_name='katildigi_etkinlikler', blank=True, verbose_name='Katılımcılar')
    olusturan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='olusturdugu_etkinlikler', verbose_name='Oluşturan')
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Etkinlik'
        verbose_name_plural = 'Etkinlikler'
        ordering = ['-tarih']
    
    def __str__(self):
        return self.baslik
    
    def katilimci_sayisi(self):
        return self.katilimcilar.count()

class Kulup(models.Model):
    KATEGORI_SECENEKLERI = [
        ('teknoloji', 'Teknoloji'),
        ('spor', 'Spor'),
        ('sanat', 'Sanat'),
        ('sosyal', 'Sosyal'),
        ('akademik', 'Akademik'),
    ]
    
    ad = models.CharField(max_length=200, verbose_name='Kulüp Adı')
    aciklama = models.TextField(verbose_name='Açıklama')
    kategori = models.CharField(max_length=20, choices=KATEGORI_SECENEKLERI, verbose_name='Kategori')
    uyeler = models.ManyToManyField(User, related_name='kulupleri', blank=True, verbose_name='Üyeler')
    kurucu = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kurucusu_oldugu_kulupler', verbose_name='Kurucu')
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Kulüp'
        verbose_name_plural = 'Kulüpler'
        ordering = ['ad']
    
    def __str__(self):
        return self.ad
    
    def uye_sayisi(self):
        return self.uyeler.count()

class Duyuru(models.Model):
    KATEGORI_SECENEKLERI = [
        ('genel', 'Genel'),
        ('akademik', 'Akademik'),
        ('sosyal', 'Sosyal'),
        ('acil', 'Acil'),
    ]
    
    baslik = models.CharField(max_length=200, verbose_name='Başlık')
    icerik = models.TextField(verbose_name='İçerik')
    kategori = models.CharField(max_length=20, choices=KATEGORI_SECENEKLERI, default='genel', verbose_name='Kategori')
    yazar = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Yazar')
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)
    goruntulenme = models.IntegerField(default=0, verbose_name='Görüntülenme')
    
    class Meta:
        verbose_name = 'Duyuru'
        verbose_name_plural = 'Duyurular'
        ordering = ['-olusturma_tarihi']
    
    def __str__(self):
        return self.baslik
