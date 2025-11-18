import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DoEvent.settings')
django.setup()

from django.contrib.auth.models import User
from Akademik.RandevuSistemi.models import Ogretmen

# Örnek öğretim görevlileri
ogretmenler = [
    {
        'username': 'ahmet.yilmaz',
        'first_name': 'Ahmet',
        'last_name': 'Yılmaz',
        'email': 'ahmet.yilmaz@university.edu.tr',
        'unvan': 'Prof. Dr.',
        'bolum': 'Bilgisayar Mühendisliği',
        'ofis': 'A Blok, Kat 3, Oda 305',
        'telefon': '+90 555 100 0001'
    },
    {
        'username': 'ayse.demir',
        'first_name': 'Ayşe',
        'last_name': 'Demir',
        'email': 'ayse.demir@university.edu.tr',
        'unvan': 'Doç. Dr.',
        'bolum': 'Bilgisayar Mühendisliği',
        'ofis': 'A Blok, Kat 3, Oda 308',
        'telefon': '+90 555 100 0002'
    },
    {
        'username': 'mehmet.kaya',
        'first_name': 'Mehmet',
        'last_name': 'Kaya',
        'email': 'mehmet.kaya@university.edu.tr',
        'unvan': 'Dr. Öğr. Üyesi',
        'bolum': 'Yazılım Mühendisliği',
        'ofis': 'A Blok, Kat 2, Oda 205',
        'telefon': '+90 555 100 0003'
    },
    {
        'username': 'fatma.sahin',
        'first_name': 'Fatma',
        'last_name': 'Şahin',
        'email': 'fatma.sahin@university.edu.tr',
        'unvan': 'Dr. Öğr. Üyesi',
        'bolum': 'Bilgisayar Mühendisliği',
        'ofis': 'B Blok, Kat 1, Oda 107',
        'telefon': '+90 555 100 0004'
    },
    {
        'username': 'ali.ozturk',
        'first_name': 'Ali',
        'last_name': 'Öztürk',
        'email': 'ali.ozturk@university.edu.tr',
        'unvan': 'Öğr. Gör.',
        'bolum': 'Bilgisayar Programcılığı',
        'ofis': 'C Blok, Kat 2, Oda 210',
        'telefon': '+90 555 100 0005'
    },
    {
        'username': 'zeynep.celik',
        'first_name': 'Zeynep',
        'last_name': 'Çelik',
        'email': 'zeynep.celik@university.edu.tr',
        'unvan': 'Prof. Dr.',
        'bolum': 'Yazılım Mühendisliği',
        'ofis': 'A Blok, Kat 4, Oda 402',
        'telefon': '+90 555 100 0006'
    },
    {
        'username': 'can.arslan',
        'first_name': 'Can',
        'last_name': 'Arslan',
        'email': 'can.arslan@university.edu.tr',
        'unvan': 'Arş. Gör. Dr.',
        'bolum': 'Bilgisayar Mühendisliği',
        'ofis': 'B Blok, Kat 2, Oda 215',
        'telefon': '+90 555 100 0007'
    },
    {
        'username': 'elif.kurt',
        'first_name': 'Elif',
        'last_name': 'Kurt',
        'email': 'elif.kurt@university.edu.tr',
        'unvan': 'Doç. Dr.',
        'bolum': 'Yazılım Mühendisliği',
        'ofis': 'A Blok, Kat 3, Oda 312',
        'telefon': '+90 555 100 0008'
    },
    {
        'username': 'emre.polat',
        'first_name': 'Emre',
        'last_name': 'Polat',
        'email': 'emre.polat@university.edu.tr',
        'unvan': 'Öğr. Gör. Dr.',
        'bolum': 'Bilgisayar Mühendisliği',
        'ofis': 'C Blok, Kat 1, Oda 105',
        'telefon': '+90 555 100 0009'
    },
    {
        'username': 'selin.yildiz',
        'first_name': 'Selin',
        'last_name': 'Yıldız',
        'email': 'selin.yildiz@university.edu.tr',
        'unvan': 'Arş. Gör.',
        'bolum': 'Bilgisayar Programcılığı',
        'ofis': 'B Blok, Kat 3, Oda 320',
        'telefon': '+90 555 100 0010'
    }
]

print("Öğretim görevlileri ekleniyor...\n")

eklenen = 0
zaten_var = 0

for ogretmen_data in ogretmenler:
    try:
        # Kullanıcı var mı kontrol et
        user, created = User.objects.get_or_create(
            username=ogretmen_data['username'],
            defaults={
                'first_name': ogretmen_data['first_name'],
                'last_name': ogretmen_data['last_name'],
                'email': ogretmen_data['email'],
                'is_staff': True,
                'is_active': True
            }
        )
        
        if created:
            user.set_password('ogrenci123')  # Varsayılan şifre
            user.save()
        
        # Öğretmen kaydı var mı kontrol et
        if not hasattr(user, 'ogretmen'):
            Ogretmen.objects.create(
                kullanici=user,
                unvan=ogretmen_data['unvan'],
                bolum=ogretmen_data['bolum'],
                ofis=ogretmen_data['ofis'],
                telefon=ogretmen_data['telefon']
            )
            print(f"✓ {ogretmen_data['unvan']} {ogretmen_data['first_name']} {ogretmen_data['last_name']} eklendi")
            eklenen += 1
        else:
            print(f"○ {ogretmen_data['unvan']} {ogretmen_data['first_name']} {ogretmen_data['last_name']} zaten kayıtlı")
            zaten_var += 1
            
    except Exception as e:
        print(f"✗ Hata ({ogretmen_data['username']}): {str(e)}")

print(f"\n{'='*50}")
print(f"✅ Toplam {eklenen} öğretim görevlisi eklendi")
print(f"ℹ️  {zaten_var} öğretim görevlisi zaten kayıtlı")
print(f"📝 Varsayılan şifre: ogrenci123")
