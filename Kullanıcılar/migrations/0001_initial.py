
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Kullanici',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kullanici_adi', models.CharField(max_length=150, unique=True, verbose_name='Kullanıcı Adı')),
                ('sifre', models.CharField(max_length=128, verbose_name='Şifre')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='E-posta')),
                ('rol', models.CharField(choices=[('user', 'Normal Kullanıcı'), ('superadmin', 'Süper Admin'), ('club_moderator', 'Kulüp Yetkilisi')], default='user', max_length=20, verbose_name='Rol')),
                ('aktif', models.BooleanField(default=True, verbose_name='Aktif')),
                ('olusturma_tarihi', models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')),
                ('son_giris', models.DateTimeField(blank=True, null=True, verbose_name='Son Giriş')),
            ],
            options={
                'verbose_name': 'Kullanıcı',
                'verbose_name_plural': 'Kullanıcılar',
                'db_table': 'kullanicilar',
                'ordering': ['-olusturma_tarihi'],
            },
        ),
    ]
