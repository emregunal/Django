"""
Admin Authentication
Simple authentication for admin panel
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from decouple import config

# Admin credentials
ADMIN_USERS = {
    config('ADMIN_USERNAME_1', default='admin'): config('ADMIN_PASSWORD_1', default='admin123'),
    config('ADMIN_USERNAME_2', default='superadmin'): config('ADMIN_PASSWORD_2', default='super123'),
}

def admin_required(view_func):
    """Decorator to check if user is admin"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('is_admin'):
            messages.error(request, 'Bu sayfaya erişim için admin girişi gereklidir.')
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)
    return wrapper

def authenticate_admin(username, password):
    """Authenticate admin user"""
    return ADMIN_USERS.get(username) == password
