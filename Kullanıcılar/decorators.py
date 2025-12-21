"""
Custom authentication decorators for Kullanici model
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def kullanici_login_required(view_func):
    """
    Decorator to check if user is logged in using custom Kullanici model
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('is_authenticated'):
            messages.error(request, 'Bu sayfayı görüntülemek için giriş yapmalısınız.')
            return redirect('kullanicilar:login')
        return view_func(request, *args, **kwargs)
    return wrapper
