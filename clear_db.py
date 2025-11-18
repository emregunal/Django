"""
Database'deki tüm örnek verileri temizleyen script
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DoEvent.settings')
django.setup()

from Akademik.AkademikTakvim.models import AkademikEtkinlik
from Akademik.DevamsizlikTakvimi.models import Ders, Devamsizlik
from Akademik.RandevuSistemi.models import Ogretmen, Randevu
from Sosyal.models import Etkinlik, Kulup, Duyuru

print("🗑️  Database'deki örnek veriler temizleniyor...")

# Sosyal modül verilerini tamamen sil
etkinlik_count = Etkinlik.objects.all().count()
Etkinlik.objects.all().delete()
print(f"✓ {etkinlik_count} etkinlik silindi")

kulup_count = Kulup.objects.all().count()
Kulup.objects.all().delete()
print(f"✓ {kulup_count} kulüp silindi")

duyuru_count = Duyuru.objects.all().count()
Duyuru.objects.all().delete()
print(f"✓ {duyuru_count} duyuru silindi")

# Akademik modül verilerini sil
akademik_count = AkademikEtkinlik.objects.all().count()
AkademikEtkinlik.objects.all().delete()
print(f"✓ {akademik_count} akademik etkinlik silindi")

randevu_count = Randevu.objects.all().count()
Randevu.objects.all().delete()
print(f"✓ {randevu_count} randevu silindi")

devamsizlik_count = Devamsizlik.objects.all().count()
Devamsizlik.objects.all().delete()
print(f"✓ {devamsizlik_count} devamsızlık kaydı silindi")

ogretmen_count = Ogretmen.objects.all().count()
Ogretmen.objects.all().delete()
print(f"✓ {ogretmen_count} öğretmen silindi")

ders_count = Ders.objects.all().count()
Ders.objects.all().delete()
print(f"✓ {ders_count} ders silindi")

print("\n✅ Tüm örnek veriler başarıyla temizlendi!")
print("📝 Kullanıcı hesapları korundu (admin ve test kullanıcıları hala aktif)")
