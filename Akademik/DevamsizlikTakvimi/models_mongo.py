from mongoengine import Document, StringField, IntField, DateTimeField

class Ders(Document):
    """
    Ders modeli - MongoEngine Document olarak yeniden yazıldı
    """
    ders_kodu = StringField(max_length=20, required=True, unique=True, verbose_name='Ders Kodu')
    ders_adi = StringField(max_length=200, required=True, verbose_name='Ders Adı')
    ogretmen = StringField(max_length=200, required=True, verbose_name='Öğretmen')
    kredi = IntField(default=3, verbose_name='Kredi')
    haftalik_ders_saati = IntField(default=3, verbose_name='Haftalık Ders Saati')
    devam_zorunlulugu = IntField(default=70, verbose_name='Devam Zorunluluğu (%)')
    
    meta = {
        'collection': 'dersler',
        'indexes': ['ders_kodu', 'ogretmen']
    }
    
    def __str__(self):
        return f"{self.ders_kodu} - {self.ders_adi}"
    
    def toplam_ders_saati(self):
        return self.haftalik_ders_saati * 14


class Devamsizlik(Document):
    """
    Devamsızlık modeli - MongoEngine Document olarak yeniden yazıldı
    """
    ogrenci_id = IntField(required=True, verbose_name='Öğrenci ID')
    ders_kodu = StringField(max_length=20, required=True, verbose_name='Ders Kodu')  # Ders referansı
    devamsiz_saat = IntField(default=0, verbose_name='Devamsız Kalınan Saat')
    tarih = StringField(verbose_name='Kayıt Tarihi')
    aciklama = StringField(verbose_name='Açıklama')
    olusturma_tarihi = DateTimeField(verbose_name='Oluşturma Tarihi')
    
    meta = {
        'collection': 'devamsizliklar',
        'ordering': ['-tarih'],
        'indexes': [
            ('ogrenci_id', 'ders_kodu'),  # Composite index for uniqueness simulation
            'ogrenci_id',
            'ders_kodu'
        ]
    }
    
    def __str__(self):
        return f"Öğrenci {self.ogrenci_id} - Ders {self.ders_kodu}"
    
    def devamsizlik_yuzdesi(self, ders):
        """
        ders: Ders document instance
        """
        toplam_saat = ders.toplam_ders_saati()
        if toplam_saat > 0:
            devamsizlik_orani = (self.devamsiz_saat / toplam_saat) * 100
            return round(100 - devamsizlik_orani, 1)
        return 100
    
    def kalan_devamsizlik_hakki(self, ders):
        """
        ders: Ders document instance
        """
        toplam_saat = ders.toplam_ders_saati()
        izin_verilen_devamsizlik = toplam_saat * (100 - ders.devam_zorunlulugu) / 100
        return max(0, int(izin_verilen_devamsizlik - self.devamsiz_saat))
