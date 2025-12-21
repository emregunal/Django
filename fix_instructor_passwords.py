import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DoEvent.settings')
import django
django.setup()

from Kullanıcılar.models import Kullanici
from Core.mongodb_utils import get_db

db = get_db()
ogretmenler = list(db.ogretmenler.find())

print("Ogretmen sifreleri guncelleniyor...")
for o in ogretmenler:
    email = o.get('email')
    ad = o.get('ad')
    if email and ad:
        try:
            user = Kullanici.objects.get(kullanici_adi=email)
            user.set_password(ad)
            user.save()
            print(f"  {email}: sifre = {ad}")
        except Kullanici.DoesNotExist:
            print(f"  {email}: kullanici bulunamadi")

print("\nTamamlandi!")
