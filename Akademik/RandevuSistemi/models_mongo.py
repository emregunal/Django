from mongoengine import Document, StringField, IntField, DateTimeField

class Ogretmen(Document):
    """
    Öğretmen modeli - MongoEngine Document olarak yeniden yazıldı
    """
    kullanici_id = IntField(required=True, unique=True, verbose_name='Kullanıcı ID')
    unvan = StringField(max_length=100, required=True, verbose_name='Ünvan')
    bolum = StringField(max_length=200, required=True, verbose_name='Bölüm')
    ofis = StringField(max_length=100, verbose_name='Ofis')
    telefon = StringField(max_length=20, verbose_name='Telefon')
    
    meta = {
        'collection': 'ogretmenler',
        'indexes': ['kullanici_id', 'bolum']
    }
    
    def __str__(self):
        return f"{self.unvan} - ID: {self.kullanici_id}"


class Randevu(Document):
    """
    Randevu modeli - MongoEngine Document olarak yeniden yazıldı
    """
    DURUM_SECENEKLERI = [
        ('bekliyor', 'Onay Bekliyor'),
        ('onaylandi', 'Onaylandı'),
        ('reddedildi', 'Reddedildi'),
        ('tamamlandi', 'Tamamlandı'),
        ('iptal', 'İptal Edildi'),
    ]
    
    ogrenci_id = IntField(required=True, verbose_name='Öğrenci ID')
    ogretmen_id = IntField(required=True, verbose_name='Öğretmen ID')
    tarih = StringField(required=True, verbose_name='Tarih')
    baslangic_saati = StringField(required=True, verbose_name='Başlangıç Saati')
    bitis_saati = StringField(required=True, verbose_name='Bitiş Saati')
    konu = StringField(max_length=200, required=True, verbose_name='Konu')
    aciklama = StringField(verbose_name='Açıklama')
    durum = StringField(max_length=20, choices=DURUM_SECENEKLERI, default='bekliyor', verbose_name='Durum')
    olusturma_tarihi = DateTimeField(verbose_name='Oluşturma Tarihi')
    guncelleme_tarihi = DateTimeField(verbose_name='Güncelleme Tarihi')
    
    meta = {
        'collection': 'randevular',
        'ordering': ['-tarih', '-baslangic_saati'],
        'indexes': ['ogrenci_id', 'ogretmen_id', 'tarih', 'durum']
    }
    
    def __str__(self):
        return f"Öğrenci {self.ogrenci_id} - Öğretmen {self.ogretmen_id} - {self.tarih}"
