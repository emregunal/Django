
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AkademikEtkinlik',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('baslik', models.CharField(max_length=200, verbose_name='Başlık')),
                ('aciklama', models.TextField(verbose_name='Açıklama')),
                ('tarih', models.DateField(verbose_name='Tarih')),
                ('baslangic_saati', models.TimeField(blank=True, null=True, verbose_name='Başlangıç Saati')),
                ('bitis_saati', models.TimeField(blank=True, null=True, verbose_name='Bitiş Saati')),
                ('tip', models.CharField(choices=[('sinav', 'Sınav'), ('odev', 'Ödev Teslim'), ('proje', 'Proje Sunumu'), ('tatil', 'Tatil'), ('diger', 'Diğer')], default='diger', max_length=20, verbose_name='Etkinlik Tipi')),
                ('konum', models.CharField(blank=True, max_length=200, verbose_name='Konum')),
                ('olusturma_tarihi', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Akademik Etkinlik',
                'verbose_name_plural': 'Akademik Etkinlikler',
                'ordering': ['tarih', 'baslangic_saati'],
            },
        ),
    ]
