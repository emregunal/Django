import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DoEvent.settings')
django.setup()

from Akademik.AkademikTakvim.models import AkademikEtkinlik
from datetime import date

# Veritabanını temizle
AkademikEtkinlik.objects.all().delete()
print("Mevcut akademik etkinlikler temizlendi.")

# 2025-2026 Akademik Takvim Verileri
akademik_etkinlikler = [
    # Güz Dönemi 2025-2026
    {
        'baslik': 'Güz Dönemi Ders Kayıtları',
        'aciklama': 'Ders ekleme-çıkarma işlemleri',
        'tarih': date(2025, 9, 15),
        'tip': 'diger',
        'konum': 'Online - Öğrenci İşleri'
    },
    {
        'baslik': 'Güz Dönemi Derslerin Başlaması',
        'aciklama': 'Güz dönemi akademik derslerinin başlangıcı',
        'tarih': date(2025, 9, 22),
        'tip': 'diger',
        'konum': 'Kampüs'
    },
    {
        'baslik': 'Güz Dönemi Ders Ekleme-Çıkarma',
        'aciklama': 'Son ders ekleme ve çıkarma tarihi',
        'tarih': date(2025, 10, 3),
        'tip': 'diger',
        'konum': 'Online - Öğrenci İşleri'
    },
    {
        'baslik': 'Cumhuriyet Bayramı Tatili',
        'aciklama': '29 Ekim Cumhuriyet Bayramı Tatili',
        'tarih': date(2025, 10, 29),
        'tip': 'tatil',
        'konum': 'Kampüs Kapalı'
    },
    {
        'baslik': 'Güz Dönemi Ara Sınav Haftası',
        'aciklama': 'Ara sınav ve değerlendirme haftası',
        'tarih': date(2025, 11, 10),
        'tip': 'sinav',
        'konum': 'Kampüs - Sınav Salonları'
    },
    {
        'baslik': 'Güz Dönemi Derslerin Bitmesi',
        'aciklama': 'Güz dönemi son ders günü',
        'tarih': date(2026, 1, 9),
        'tip': 'diger',
        'konum': 'Kampüs'
    },
    {
        'baslik': 'Güz Dönemi Final Sınavları',
        'aciklama': 'Final sınav dönemi',
        'tarih': date(2026, 1, 12),
        'tip': 'sinav',
        'konum': 'Kampüs - Sınav Salonları'
    },
    {
        'baslik': 'Güz Dönemi Bütünleme Sınavları',
        'aciklama': 'Bütünleme/Tek ders sınavları',
        'tarih': date(2026, 1, 26),
        'tip': 'sinav',
        'konum': 'Kampüs - Sınav Salonları'
    },
    
    # Bahar Dönemi 2025-2026
    {
        'baslik': 'Bahar Dönemi Ders Kayıtları',
        'aciklama': 'Ders ekleme-çıkarma işlemleri',
        'tarih': date(2026, 2, 2),
        'tip': 'diger',
        'konum': 'Online - Öğrenci İşleri'
    },
    {
        'baslik': 'Bahar Dönemi Derslerin Başlaması',
        'aciklama': 'Bahar dönemi akademik derslerinin başlangıcı',
        'tarih': date(2026, 2, 9),
        'tip': 'diger',
        'konum': 'Kampüs'
    },
    {
        'baslik': 'Bahar Dönemi Ders Ekleme-Çıkarma',
        'aciklama': 'Son ders ekleme ve çıkarma tarihi',
        'tarih': date(2026, 2, 20),
        'tip': 'diger',
        'konum': 'Online - Öğrenci İşleri'
    },
    {
        'baslik': 'Ramazan Bayramı Tatili',
        'aciklama': 'Ramazan Bayramı Tatili (9 gün)',
        'tarih': date(2026, 3, 20),
        'tip': 'tatil',
        'konum': 'Kampüs Kapalı'
    },
    {
        'baslik': 'Bahar Dönemi Ara Sınav Haftası',
        'aciklama': 'Ara sınav ve değerlendirme haftası',
        'tarih': date(2026, 4, 6),
        'tip': 'sinav',
        'konum': 'Kampüs - Sınav Salonları'
    },
    {
        'baslik': 'Ulusal Egemenlik ve Çocuk Bayramı',
        'aciklama': '23 Nisan Tatili',
        'tarih': date(2026, 4, 23),
        'tip': 'tatil',
        'konum': 'Kampüs Kapalı'
    },
    {
        'baslik': 'İşçi Bayramı Tatili',
        'aciklama': '1 Mayıs Emek ve Dayanışma Günü',
        'tarih': date(2026, 5, 1),
        'tip': 'tatil',
        'konum': 'Kampüs Kapalı'
    },
    {
        'baslik': 'Gençlik ve Spor Bayramı',
        'aciklama': '19 Mayıs Tatili',
        'tarih': date(2026, 5, 19),
        'tip': 'tatil',
        'konum': 'Kampüs Kapalı'
    },
    {
        'baslik': 'Bahar Dönemi Derslerin Bitmesi',
        'aciklama': 'Bahar dönemi son ders günü',
        'tarih': date(2026, 5, 29),
        'tip': 'diger',
        'konum': 'Kampüs'
    },
    {
        'baslik': 'Bahar Dönemi Final Sınavları',
        'aciklama': 'Final sınav dönemi',
        'tarih': date(2026, 6, 1),
        'tip': 'sinav',
        'konum': 'Kampüs - Sınav Salonları'
    },
    {
        'baslik': 'Kurban Bayramı Tatili',
        'aciklama': 'Kurban Bayramı Tatili (9 gün)',
        'tarih': date(2026, 5, 27),
        'tip': 'tatil',
        'konum': 'Kampüs Kapalı'
    },
    {
        'baslik': 'Bahar Dönemi Bütünleme Sınavları',
        'aciklama': 'Bütünleme/Tek ders sınavları',
        'tarih': date(2026, 6, 22),
        'tip': 'sinav',
        'konum': 'Kampüs - Sınav Salonları'
    },
    
    # Yaz Dönemi 2025-2026
    {
        'baslik': 'Yaz Dönemi Ders Kayıtları',
        'aciklama': 'Yaz okulu ders kayıtları',
        'tarih': date(2026, 6, 29),
        'tip': 'diger',
        'konum': 'Online - Öğrenci İşleri'
    },
    {
        'baslik': 'Yaz Dönemi Derslerin Başlaması',
        'aciklama': 'Yaz okulu derslerinin başlangıcı',
        'tarih': date(2026, 7, 6),
        'tip': 'diger',
        'konum': 'Kampüs'
    },
    {
        'baslik': 'Zafer Bayramı Tatili',
        'aciklama': '30 Ağustos Zafer Bayramı',
        'tarih': date(2026, 8, 30),
        'tip': 'tatil',
        'konum': 'Kampüs Kapalı'
    },
    {
        'baslik': 'Yaz Dönemi Final Sınavları',
        'aciklama': 'Yaz okulu final sınavları',
        'tarih': date(2026, 8, 31),
        'tip': 'sinav',
        'konum': 'Kampüs - Sınav Salonları'
    },
]

# Verileri ekle
created_count = 0
for etkinlik_data in akademik_etkinlikler:
    AkademikEtkinlik.objects.create(**etkinlik_data)
    created_count += 1
    print(f"✓ {etkinlik_data['baslik']} - {etkinlik_data['tarih']}")

print(f"\n✅ Toplam {created_count} akademik etkinlik başarıyla eklendi!")
