
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Kullanıcılar', '0002_kullanici_bolum_kullanici_isim_alter_kullanici_rol'),
    ]

    operations = [
        migrations.AddField(
            model_name='kullanici',
            name='okul_numarasi',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Okul Numarası'),
        ),
    ]
