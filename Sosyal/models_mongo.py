from mongoengine import Document, StringField, DateTimeField, ListField, IntField
from django.contrib.auth.models import User

class Etkinlik(Document):
    """
    Sosyal etkinlik modeli - MongoEngine Document olarak yeniden yazıldı
    """
    KATEGORI_SECENEKLERI = [
        ('konser', 'Konser'),
        ('konferans', 'Konferans'),
        ('spor', 'Spor'),
        ('sosyal', 'Sosyal'),
        ('akademik', 'Akademik'),
        ('tiyatro', 'Tiyatro'),
    ]
    
    baslik = StringField(max_length=200, required=True, verbose_name='Başlık')
    aciklama = StringField(required=True, verbose_name='Açıklama')
    kategori = StringField(max_length=20, choices=KATEGORI_SECENEKLERI, required=True, verbose_name='Kategori')
    tarih = StringField(required=True, verbose_name='Tarih')
    baslangic_saati = StringField(required=True, verbose_name='Başlangıç Saati')
    bitis_saati = StringField(required=True, verbose_name='Bitiş Saati')
    konum = StringField(max_length=200, required=True, verbose_name='Konum')
    katilimci_ids = ListField(IntField(), verbose_name='Katılımcı IDs')
    olusturan_id = IntField(required=True, verbose_name='Oluşturan ID')
    olusturma_tarihi = DateTimeField(verbose_name='Oluşturma Tarihi')
    
    meta = {
        'collection': 'etkinlikler',
        'ordering': ['-tarih'],
        'indexes': ['tarih', 'kategori']
    }
    
    def __str__(self):
        return self.baslik
    
    def katilimci_sayisi(self):
        return len(self.katilimci_ids) if self.katilimci_ids else 0


class Kulup(Document):
    """
    Kulüp modeli - MongoEngine Document olarak yeniden yazıldı
    """
    KATEGORI_SECENEKLERI = [
        ('teknoloji', 'Teknoloji'),
        ('spor', 'Spor'),
        ('sanat', 'Sanat'),
        ('sosyal', 'Sosyal'),
        ('akademik', 'Akademik'),
    ]
    
    ad = StringField(max_length=200, required=True, verbose_name='Kulüp Adı')
    aciklama = StringField(required=True, verbose_name='Açıklama')
    kategori = StringField(max_length=20, choices=KATEGORI_SECENEKLERI, required=True, verbose_name='Kategori')
    uye_ids = ListField(IntField(), verbose_name='Üye IDs')
    kurucu_id = IntField(required=True, verbose_name='Kurucu ID')
    olusturma_tarihi = DateTimeField(verbose_name='Oluşturma Tarihi')
    
    meta = {
        'collection': 'kulupler',
        'ordering': ['ad'],
        'indexes': ['ad', 'kategori']
    }
    
    def __str__(self):
        return self.ad
    
    def uye_sayisi(self):
        return len(self.uye_ids) if self.uye_ids else 0


class Duyuru(Document):
    """
    Duyuru modeli - MongoEngine Document olarak yeniden yazıldı
    """
    KATEGORI_SECENEKLERI = [
        ('genel', 'Genel'),
        ('akademik', 'Akademik'),
        ('sosyal', 'Sosyal'),
        ('acil', 'Acil'),
    ]
    
    baslik = StringField(max_length=200, required=True, verbose_name='Başlık')
    icerik = StringField(required=True, verbose_name='İçerik')
    kategori = StringField(max_length=20, choices=KATEGORI_SECENEKLERI, default='genel', verbose_name='Kategori')
    yazar_id = IntField(required=True, verbose_name='Yazar ID')
    olusturma_tarihi = DateTimeField(verbose_name='Oluşturma Tarihi')
    goruntulenme = IntField(default=0, verbose_name='Görüntülenme')
    
    meta = {
        'collection': 'duyurular',
        'ordering': ['-olusturma_tarihi'],
        'indexes': ['kategori', '-olusturma_tarihi']
    }
    
    def __str__(self):
        return self.baslik
