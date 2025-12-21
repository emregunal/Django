from mongoengine import Document, StringField, IntField, DateTimeField

class AkademikEtkinlik(Document):
    """
    Akademik etkinlik modeli - MongoEngine Document olarak yeniden yazıldı
    """
    ETKINLIK_TIPLERI = [
        ('sinav', 'Sınav'),
        ('odev', 'Ödev Teslim'),
        ('proje', 'Proje Sunumu'),
        ('tatil', 'Tatil'),
        ('diger', 'Diğer'),
    ]
    
    baslik = StringField(max_length=200, required=True, verbose_name='Başlık')
    aciklama = StringField(required=True, verbose_name='Açıklama')
    tarih = StringField(required=True, verbose_name='Tarih')
    baslangic_saati = StringField(verbose_name='Başlangıç Saati')
    bitis_saati = StringField(verbose_name='Bitiş Saati')
    tip = StringField(max_length=20, choices=ETKINLIK_TIPLERI, default='diger', verbose_name='Etkinlik Tipi')
    konum = StringField(max_length=200, verbose_name='Konum')
    olusturma_tarihi = DateTimeField(verbose_name='Oluşturma Tarihi')
    
    meta = {
        'collection': 'akademik_etkinlikler',
        'ordering': ['tarih', 'baslangic_saati'],
        'indexes': ['tarih', 'tip']
    }
    
    def __str__(self):
        return f"{self.baslik} - {self.tarih}"
