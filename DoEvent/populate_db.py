"""
Database'i örnek verilerle dolduran script
Kullanım: python manage.py shell < populate_db.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DoEvent.settings')
django.setup()

from django.contrib.auth.models import User
from Akademik.AkademikTakvim.models import AkademikEtkinlik
from Akademik.DevamsizlikTakvimi.models import Ders, Devamsizlik
from Akademik.RandevuSistemi.models import Ogretmen, Randevu
from Sosyal.models import Etkinlik, Kulup, Duyuru
from datetime import datetime, timedelta, time

print("🚀 Database'e örnek veriler ekleniyor...")

# Kullanıcılar oluştur
try:
    admin_user = User.objects.get(username='admin')
    print("✓ Admin kullanıcı zaten var")
except User.DoesNotExist:
    admin_user = User.objects.create_superuser('admin', 'admin@doevent.com', 'admin123')
    print("✓ Admin kullanıcı oluşturuldu (admin/admin123)")

try:
    test_user = User.objects.get(username='test')
    print("✓ Test kullanıcı zaten var")
except User.DoesNotExist:
    test_user = User.objects.create_user('test', 'test@doevent.com', 'test123', first_name='Test', last_name='Kullanıcı')
    print("✓ Test kullanıcı oluşturuldu (test/test123)")

# Akademik Etkinlikler
bugun = datetime.now().date()
etkinlikler_data = [
    {'baslik': 'Vize Sınavı - Matematik I', 'tip': 'sinav', 'tarih': bugun + timedelta(days=7), 'baslangic_saati': time(9, 0), 'bitis_saati': time(11, 0), 'konum': 'A-101', 'aciklama': 'Matematik I dersi vize sınavı'},
    {'baslik': 'Proje Sunumu - Yazılım Mühendisliği', 'tip': 'proje', 'tarih': bugun + timedelta(days=10), 'baslangic_saati': time(14, 0), 'bitis_saati': time(16, 0), 'konum': 'B-205', 'aciklama': 'Dönem projesi sunumları'},
    {'baslik': 'Ödev Teslim - Fizik II', 'tip': 'odev', 'tarih': bugun + timedelta(days=5), 'baslangic_saati': time(23, 59), 'konum': 'Online', 'aciklama': 'Fizik II ödev teslimi'},
    {'baslik': 'Ara Tatil', 'tip': 'tatil', 'tarih': bugun + timedelta(days=14), 'bitis_saati': time(23, 59), 'aciklama': 'Yarıyıl tatili başlangıcı'},
    {'baslik': 'Final Sınavı - Veritabanı', 'tip': 'sinav', 'tarih': bugun + timedelta(days=21), 'baslangic_saati': time(10, 0), 'bitis_saati': time(12, 0), 'konum': 'C-301', 'aciklama': 'Veritabanı dersi final sınavı'},
]

for etk_data in etkinlikler_data:
    AkademikEtkinlik.objects.get_or_create(
        baslik=etk_data['baslik'],
        defaults=etk_data
    )
print(f"✓ {len(etkinlikler_data)} akademik etkinlik eklendi")

# Dersler
dersler_data = [
    {'ders_kodu': 'MAT101', 'ders_adi': 'Matematik I', 'ogretmen': 'Prof. Dr. Ahmet Yılmaz', 'kredi': 4},
    {'ders_kodu': 'FIZ102', 'ders_adi': 'Fizik II', 'ogretmen': 'Doç. Dr. Ayşe Demir', 'kredi': 3},
    {'ders_kodu': 'BIL201', 'ders_adi': 'Veri Yapıları', 'ogretmen': 'Dr. Öğr. Üyesi Mehmet Kaya', 'kredi': 4},
    {'ders_kodu': 'YAZ301', 'ders_adi': 'Yazılım Mühendisliği', 'ogretmen': 'Prof. Dr. Fatma Çelik', 'kredi': 3},
]

dersler = []
for ders_data in dersler_data:
    ders, created = Ders.objects.get_or_create(
        ders_kodu=ders_data['ders_kodu'],
        defaults=ders_data
    )
    dersler.append(ders)
print(f"✓ {len(dersler_data)} ders eklendi")

# Devamsızlıklar
devamsizlik_count = 0
for ders in dersler[:2]:  # İlk 2 ders için
    for i in range(2):  # Her ders için 2 devamsızlık
        Devamsizlik.objects.get_or_create(
            ogrenci=test_user,
            ders=ders,
            tarih=bugun - timedelta(days=7*(i+1)),
            defaults={'mazeret': i % 2 == 0, 'aciklama': 'Hastalık' if i % 2 == 0 else ''}
        )
        devamsizlik_count += 1
print(f"✓ {devamsizlik_count} devamsızlık kaydı eklendi")

# Öğretmenler
ogretmenler_data = [
    {'kullanici': admin_user, 'unvan': 'Prof. Dr.', 'bolum': 'Bilgisayar Mühendisliği', 'ofis': 'A-301', 'telefon': '555-0101'},
]

ogretmenler = []
for ogt_data in ogretmenler_data:
    ogt, created = Ogretmen.objects.get_or_create(
        kullanici=ogt_data['kullanici'],
        defaults=ogt_data
    )
    ogretmenler.append(ogt)
print(f"✓ {len(ogretmenler_data)} öğretmen eklendi")

# Randevular
if ogretmenler:
    randevular_data = [
        {'tarih': bugun + timedelta(days=3), 'baslangic_saati': time(10, 0), 'bitis_saati': time(10, 30), 'konu': 'Proje Danışmanlığı', 'aciklama': 'Dönem projesi hakkında', 'durum': 'onaylandi'},
        {'tarih': bugun + timedelta(days=8), 'baslangic_saati': time(14, 0), 'bitis_saati': time(14, 30), 'konu': 'Ders Danışmanlığı', 'aciklama': 'Ders seçimi', 'durum': 'bekliyor'},
    ]
    
    for rdv_data in randevular_data:
        Randevu.objects.get_or_create(
            ogrenci=test_user,
            ogretmen=ogretmenler[0],
            tarih=rdv_data['tarih'],
            baslangic_saati=rdv_data['baslangic_saati'],
            defaults=rdv_data
        )
    print(f"✓ {len(randevular_data)} randevu eklendi")

# Etkinlikler
etkinlikler_data = [
    {'baslik': 'Bahar Konseri 2025', 'kategori': 'konser', 'tarih': bugun + timedelta(days=7), 'baslangic_saati': time(19, 0), 'bitis_saati': time(22, 0), 'konum': 'Açık Hava Amfitiyatrosu', 'aciklama': 'Üniversitemizin geleneksel bahar konseri. Ünlü sanatçılar ve öğrenci grupları sahne alacak.'},
    {'baslik': 'Yapay Zeka ve Gelecek', 'kategori': 'konferans', 'tarih': bugun + timedelta(days=10), 'baslangic_saati': time(14, 0), 'bitis_saati': time(17, 0), 'konum': 'Konferans Salonu', 'aciklama': 'Yapay zeka alanında uzman konuşmacıların katılacağı özel konferans.'},
    {'baslik': 'Fakülteler Arası Futbol Turnuvası', 'kategori': 'spor', 'tarih': bugun + timedelta(days=12), 'baslangic_saati': time(10, 0), 'bitis_saati': time(18, 0), 'konum': 'Spor Kompleksi', 'aciklama': 'Fakülteler arasında düzenlenecek geleneksel futbol turnuvası.'},
    {'baslik': 'Sanat Atölyesi', 'kategori': 'sosyal', 'tarih': bugun + timedelta(days=14), 'baslangic_saati': time(15, 0), 'bitis_saati': time(18, 0), 'konum': 'Sanat Atölyesi', 'aciklama': 'Resim ve heykel atölyesi. Malzemeler ücretsiz sağlanacak.'},
    {'baslik': 'Kariyer Günleri', 'kategori': 'akademik', 'tarih': bugun + timedelta(days=17), 'baslangic_saati': time(9, 0), 'bitis_saati': time(17, 0), 'konum': 'A Blok Fuaye', 'aciklama': 'Şirket temsilcileri ile tanışma ve kariyer fırsatları.'},
    {'baslik': 'Tiyatro Gösterisi', 'kategori': 'tiyatro', 'tarih': bugun + timedelta(days=20), 'baslangic_saati': time(20, 0), 'bitis_saati': time(22, 0), 'konum': 'Kültür Merkezi', 'aciklama': 'Öğrenci tiyatro topluluğu tarafından hazırlanan özel gösteri.'},
]

for etk_data in etkinlikler_data:
    etk, created = Etkinlik.objects.get_or_create(
        baslik=etk_data['baslik'],
        defaults={**etk_data, 'olusturan': admin_user}
    )
    if created:
        # Rastgele katılımcı sayısı ekle
        import random
        for _ in range(random.randint(50, 500)):
            pass  # Gerçek uygulamada buraya kullanıcılar eklenebilir
print(f"✓ {len(etkinlikler_data)} etkinlik eklendi")

# Kulüpler
kulupler_data = [
    {'ad': 'Bilgisayar Kulübü', 'kategori': 'teknoloji', 'aciklama': 'Yazılım geliştirme, yapay zeka ve siber güvenlik konularında çalışmalar yapıyoruz.'},
    {'ad': 'Spor Kulübü', 'kategori': 'spor', 'aciklama': 'Çeşitli spor aktiviteleri ve turnuvalar düzenliyoruz.'},
    {'ad': 'Müzik Kulübü', 'kategori': 'sanat', 'aciklama': 'Müzik aletleri çalışmaları ve konserler düzenliyoruz.'},
    {'ad': 'Sosyal Sorumluluk Kulübü', 'kategori': 'sosyal', 'aciklama': 'Topluma faydalı projeler geliştiriyor ve sosyal sorumluluk projeleri yürütüyoruz.'},
    {'ad': 'Fotoğrafçılık Kulübü', 'kategori': 'sanat', 'aciklama': 'Fotoğraf çekimi, düzenleme teknikleri ve sergiler düzenliyoruz.'},
    {'ad': 'Robotik Kulübü', 'kategori': 'teknoloji', 'aciklama': 'Robot tasarımı, programlama ve yarışmalar.'},
]

for kulup_data in kulupler_data:
    Kulup.objects.get_or_create(
        ad=kulup_data['ad'],
        defaults={**kulup_data, 'kurucu': admin_user}
    )
print(f"✓ {len(kulupler_data)} kulüp eklendi")

# Duyurular
duyurular_data = [
    {'baslik': 'Kayıt Yenileme Dönemi Başladı', 'kategori': 'akademik', 'icerik': 'Güz dönemi kayıt yenileme işlemleri 1 Eylül tarihinde başlayacaktır. Öğrencilerimizin not durumlarını kontrol ederek zamanında kayıt yaptırmaları önemle duyurulur.'},
    {'baslik': 'Yeni Kütüphane Açılışı', 'kategori': 'genel', 'icerik': 'Kampüsümüze kazandırılan yeni kütüphane binası 15 Eylül Pazartesi günü hizmete açılacaktır. Açılış törenine tüm öğrencilerimiz davetlidir.'},
    {'baslik': 'Burs Başvuruları', 'kategori': 'akademik', 'icerik': 'Başarı bursu başvuruları için son tarih 20 Eylül. Başvuru şartları ve detaylı bilgi için öğrenci işleri dairesine başvurunuz.'},
    {'baslik': 'Kampüste Tadilat Çalışmaları', 'kategori': 'genel', 'icerik': 'A Blok 3. katta yapılacak tadilat çalışmaları nedeniyle 10-15 Eylül tarihleri arasında bu bölüm kapalı olacaktır.'},
    {'baslik': 'Spor Tesisleri Kullanımı', 'kategori': 'sosyal', 'icerik': 'Yeni açılan spor salonumuz hafta içi 08:00-22:00, hafta sonu 10:00-20:00 saatleri arasında öğrencilerimizin kullanımına açıktır.'},
]

for duyuru_data in duyurular_data:
    Duyuru.objects.get_or_create(
        baslik=duyuru_data['baslik'],
        defaults={**duyuru_data, 'yazar': admin_user}
    )
print(f"✓ {len(duyurular_data)} duyuru eklendi")

print("\n✅ Tüm örnek veriler başarıyla eklendi!")
print("\n📝 Giriş Bilgileri:")
print("   Admin: admin / admin123")
print("   Test Kullanıcı: test / test123")
