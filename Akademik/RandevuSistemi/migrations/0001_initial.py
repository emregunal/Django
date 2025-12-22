
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ogretmen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unvan', models.CharField(max_length=100, verbose_name='Ünvan')),
                ('bolum', models.CharField(max_length=200, verbose_name='Bölüm')),
                ('ofis', models.CharField(blank=True, max_length=100, verbose_name='Ofis')),
                ('telefon', models.CharField(blank=True, max_length=20, verbose_name='Telefon')),
                ('kullanici', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Kullanıcı')),
            ],
            options={
                'verbose_name': 'Öğretmen',
                'verbose_name_plural': 'Öğretmenler',
            },
        ),
        migrations.CreateModel(
            name='Randevu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tarih', models.DateField(verbose_name='Tarih')),
                ('baslangic_saati', models.TimeField(verbose_name='Başlangıç Saati')),
                ('bitis_saati', models.TimeField(verbose_name='Bitiş Saati')),
                ('konu', models.CharField(max_length=200, verbose_name='Konu')),
                ('aciklama', models.TextField(blank=True, verbose_name='Açıklama')),
                ('durum', models.CharField(choices=[('bekliyor', 'Onay Bekliyor'), ('onaylandi', 'Onaylandı'), ('reddedildi', 'Reddedildi'), ('tamamlandi', 'Tamamlandı'), ('iptal', 'İptal Edildi')], default='bekliyor', max_length=20, verbose_name='Durum')),
                ('olusturma_tarihi', models.DateTimeField(auto_now_add=True)),
                ('guncelleme_tarihi', models.DateTimeField(auto_now=True)),
                ('ogrenci', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='randevular', to=settings.AUTH_USER_MODEL, verbose_name='Öğrenci')),
                ('ogretmen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RandevuSistemi.ogretmen', verbose_name='Öğretmen')),
            ],
            options={
                'verbose_name': 'Randevu',
                'verbose_name_plural': 'Randevular',
                'ordering': ['-tarih', '-baslangic_saati'],
            },
        ),
    ]
