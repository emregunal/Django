from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone


class Kullanici(models.Model):
    """
    Custom user model for both main site and admin panel authentication
    """
    ROL_CHOICES = [
        ('user', 'Normal Kullanıcı'),
        ('superadmin', 'Süper Admin'),
        ('club_moderator', 'Kulüp Yetkilisi'),
        ('instructor', 'Öğretim Görevlisi'),
    ]
    
    kullanici_adi = models.CharField(max_length=150, unique=True, verbose_name='Kullanıcı Adı')
    sifre = models.CharField(max_length=128, verbose_name='Şifre')
    email = models.EmailField(blank=True, null=True, verbose_name='E-posta')
    isim = models.CharField(max_length=150, blank=True, null=True, verbose_name='Ad Soyad')
    bolum = models.CharField(max_length=200, blank=True, null=True, verbose_name='Bölüm')
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='user', verbose_name='Rol')
    aktif = models.BooleanField(default=True, verbose_name='Aktif')
    olusturma_tarihi = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    son_giris = models.DateTimeField(null=True, blank=True, verbose_name='Son Giriş')
    
    class Meta:
        db_table = 'kullanicilar'
        verbose_name = 'Kullanıcı'
        verbose_name_plural = 'Kullanıcılar'
        ordering = ['-olusturma_tarihi']
    
    def __str__(self):
        return f"{self.kullanici_adi} ({self.get_rol_display()})"
    
    def set_password(self, raw_password):
        """Hash the password and save it"""
        self.sifre = make_password(raw_password)
    
    def check_password(self, raw_password):
        """Check if the provided password matches the stored hash"""
        return check_password(raw_password, self.sifre)
    
    def update_last_login(self):
        """Update the last login timestamp"""
        self.son_giris = timezone.now()
        self.save(update_fields=['son_giris'])
    
    def is_admin(self):
        """Check if user has admin privileges"""
        return self.rol in ['superadmin', 'club_moderator']
    
    def is_superadmin(self):
        """Check if user is a superadmin"""
        return self.rol == 'superadmin'
    
    def is_club_moderator(self):
        """Check if user is a club moderator"""
        return self.rol == 'club_moderator'
