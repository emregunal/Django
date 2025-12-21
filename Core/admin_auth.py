"""
Admin Authentication with Role-Based Access Control
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from Kullanıcılar.models import Kullanici


def authenticate_admin(username, password):
    """Authenticate admin user from database and return role"""
    try:
        kullanici = Kullanici.objects.get(kullanici_adi=username)
        
        # Şifreyi kontrol et
        if not kullanici.check_password(password):
            return None
        
        # Hesap aktif mi kontrol et
        if not kullanici.aktif:
            return None
        
        # Sadece admin rollerine sahip kullanıcıların giriş yapmasına izin ver
        # club_moderator artık ayrı kulüp panelini kullanıyor
        if kullanici.rol in ['superadmin', 'instructor', 'ogretmen']:
            return kullanici.rol
        
        return None
    
    except Kullanici.DoesNotExist:
        return None

def admin_required(view_func):
    """Decorator to check if user is admin (any role)"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('is_admin'):
            messages.error(request, 'Bu sayfaya erişim için admin girişi gereklidir.')
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)
    return wrapper

def superadmin_required(view_func):
    """Decorator to check if user is superadmin"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('is_admin'):
            messages.error(request, 'Bu sayfaya erişim için admin girişi gereklidir.')
            return redirect('admin_login')
        
        role = request.session.get('admin_role')
        if role != 'superadmin':
            messages.error(request, 'Bu sayfaya erişim yetkiniz yok. Sadece superadmin erişebilir.')
            # Kulüp yetkilisi ise etkinliklere yönlendir
            if role == 'club_moderator':
                return redirect('admin_events')
            return redirect('admin_login')
        
        return view_func(request, *args, **kwargs)
    return wrapper

def club_moderator_required(view_func):
    """Decorator to check if user is club moderator or superadmin"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('is_admin'):
            messages.error(request, 'Bu sayfaya erişim için admin girişi gereklidir.')
            return redirect('admin_login')
        
        role = request.session.get('admin_role')
        if role not in ['club_moderator', 'superadmin']:
            messages.error(request, 'Bu sayfaya erişim yetkiniz yok.')
            return redirect('admin_dashboard')
        
        return view_func(request, *args, **kwargs)
    return wrapper

def instructor_required(view_func):
    """Decorator to check if user is instructor or superadmin"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('is_admin'):
            messages.error(request, 'Bu sayfaya erişim için admin girişi gereklidir.')
            return redirect('admin_login')
        
        role = request.session.get('admin_role')
        if role not in ['instructor', 'ogretmen', 'superadmin']:
            messages.error(request, 'Bu sayfaya erişim yetkiniz yok.')
            if role == 'club_moderator':
                return redirect('admin_events')
            return redirect('admin_login')
        
        return view_func(request, *args, **kwargs)
    return wrapper
