"""
Script to create initial users in the kullanicilar table
Run this script once to populate the database with initial users
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DoEvent.settings')
django.setup()

from Kullanıcılar.models import Kullanici
from decouple import config


def create_initial_users():
    """Create initial users for the system"""
    
    print("Creating initial users...")
    
    users_to_create = [
        {
            'kullanici_adi': config('ADMIN_USERNAME_1', default='admin'),
            'password': config('ADMIN_PASSWORD_1', default='admin123'),
            'email': 'admin@dogustansosyal.com',
            'rol': 'superadmin',
        },
        {
            'kullanici_adi': config('ADMIN_USERNAME_2', default='superadmin'),
            'password': config('ADMIN_PASSWORD_2', default='super123'),
            'email': 'superadmin@dogustansosyal.com',
            'rol': 'superadmin',
        },
        {
            'kullanici_adi': 'kulup1',
            'password': 'kulup123',
            'email': 'kulup1@dogustansosyal.com',
            'rol': 'club_moderator',
        },
        {
            'kullanici_adi': 'kulup2',
            'password': 'kulup123',
            'email': 'kulup2@dogustansosyal.com',
            'rol': 'club_moderator',
        },
        {
            'kullanici_adi': 'testuser',
            'password': 'test123',
            'email': '202303011100@dogus.edu.tr',
            'rol': 'user',
            'isim': 'Eren Turna',
            'bolum': 'Yazılım Mühendisliği',
            'okul_numarasi': '202303011100',
        },
        {
            'kullanici_adi': 'ogretmen1',
            'password': 'ogretmen123',
            'email': 'ogretmen1@dogustansosyal.com',
            'rol': 'instructor',
        },
    ]
    
    created_count = 0
    skipped_count = 0
    
    for user_data in users_to_create:
        kullanici_adi = user_data['kullanici_adi']
        
        if Kullanici.objects.filter(kullanici_adi=kullanici_adi).exists():
            print(f"[!] Kullanici zaten mevcut: {kullanici_adi}")
            skipped_count += 1
            continue
        
        kullanici = Kullanici(
            kullanici_adi=kullanici_adi,
            email=user_data['email'],
            rol=user_data['rol'],
            isim=user_data.get('isim', ''),
            bolum=user_data.get('bolum', ''),
            okul_numarasi=user_data.get('okul_numarasi', ''),
            aktif=True,
        )
        kullanici.set_password(user_data['password'])
        kullanici.save()
        
        print(f"[+] Kullanici olusturuldu: {kullanici_adi} ({kullanici.get_rol_display()})")

        created_count += 1
    
    print(f"\n{'='*50}")
    print(f"Toplam oluşturulan kullanıcı: {created_count}")
    print(f"Atlanan kullanıcı: {skipped_count}")
    print(f"{'='*50}\n")
    
    print("Mevcut kullanicilar:")
    print(f"{'Kullanici Adi':<20} {'Rol':<20} {'E-posta':<30} {'Aktif'}")
    print("-" * 80)
    for kullanici in Kullanici.objects.all():
        aktif_str = 'Evet' if kullanici.aktif else 'Hayir'
        print(f"{kullanici.kullanici_adi:<20} {kullanici.get_rol_display():<20} {kullanici.email or 'N/A':<30} {aktif_str}")


def create_instructor_users_from_mongodb():
    """Create instructor users from MongoDB ogretmenler collection"""
    from Core.mongodb_utils import get_db
    
    print("\n" + "="*50)
    print("MongoDB'den ogretmen kullanicilari olusturuluyor...")
    print("="*50 + "\n")
    
    db = get_db()
    
    ogretmenler = list(db.ogretmenler.find())
    
    if not ogretmenler:
        print("[!] MongoDB'de kayitli ogretmen bulunamadi.")
        return
    
    print(f"Toplam {len(ogretmenler)} ogretmen bulundu.\n")
    
    created_count = 0
    skipped_count = 0
    
    for ogretmen in ogretmenler:
        ad = ogretmen.get('ad', '')
        email = ogretmen.get('email', '')
        
        if not ad:
            print(f"[!] Ad bilgisi yok, atlaniyor: {ogretmen}")
            skipped_count += 1
            continue
        
        kullanici_adi = email if email else ad.lower().replace(' ', '_')
        
        sifre = ad
        
        if Kullanici.objects.filter(kullanici_adi=kullanici_adi).exists():
            print(f"[!] Kullanici zaten mevcut: {kullanici_adi}")
            skipped_count += 1
            continue
        
        kullanici = Kullanici.objects.create(
            kullanici_adi=kullanici_adi,
            email=email,
            rol='instructor',
            aktif=True
        )
        kullanici.set_password(sifre)
        kullanici.save()
        
        db.ogretmenler.update_one(
            {'_id': ogretmen['_id']},
            {'$set': {'kullanici_adi': kullanici_adi}}
        )
        
        print(f"[+] Ogretmen kullanici olusturuldu: {kullanici_adi} (Sifre: {sifre})")
        created_count += 1
    
    print(f"\nOgretmen sonuc: {created_count} olusturuldu, {skipped_count} atlandi")


if __name__ == '__main__':
    create_initial_users()
    create_instructor_users_from_mongodb()

