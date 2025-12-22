from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from Kullanıcılar.models import Kullanici
import json


@csrf_exempt
def register_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            
            if Kullanici.objects.filter(kullanici_adi=username).exists():
                return JsonResponse({
                    'status': 'error',
                    'message': 'Bu kullanıcı adı zaten kullanılıyor.'
                }, status=400)
                
            kullanici = Kullanici(
                kullanici_adi=username,
                email=email,
                rol='user',
                aktif=True,
            )
            kullanici.set_password(password)
            kullanici.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Kullanıcı başarıyla oluşturuldu',
                'user': {
                    'id': kullanici.id,
                    'username': kullanici.kullanici_adi,
                    'email': kullanici.email
                }
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Geçersiz JSON formatı'
            }, status=400)
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
            
    return JsonResponse({
        'status': 'error',
        'message': 'Sadece POST istekleri kabul edilir'
    }, status=405)

def login_view(request):    
    if request.session.get('is_authenticated'):
        return redirect('index')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            try:
                kullanici = Kullanici.objects.get(kullanici_adi=username)
                
                if kullanici.check_password(password):
                    if not kullanici.aktif:
                        messages.error(request, 'Hesabınız devre dışı bırakılmış.')
                        return render(request, 'kullanicilar/login.html')
                    
                    if kullanici.rol in ['superadmin', 'instructor']:
                        messages.info(request, 'Admin paneli için admin girişini kullanın.')
                        return redirect('admin_login')
                    
                    request.session['user_id'] = kullanici.id
                    request.session['user_username'] = kullanici.kullanici_adi
                    request.session['user_role'] = kullanici.rol
                    request.session['user_isim'] = kullanici.isim if kullanici.isim else kullanici.kullanici_adi
                    request.session['is_authenticated'] = True
                    
                    kullanici.update_last_login()
                    
                    messages.success(request, f'Hoş geldiniz, {kullanici.kullanici_adi}!')
                    return redirect('index')
                else:
                    messages.error(request, 'Geçersiz kullanıcı adı veya şifre.')
            
            except Kullanici.DoesNotExist:
                messages.error(request, 'Geçersiz kullanıcı adı veya şifre.')
        else:
            messages.error(request, 'Lütfen kullanıcı adı ve şifrenizi girin.')
    
    return render(request, 'kullanicilar/login.html')

def logout_view(request):
    request.session.flush()
    
    messages.success(request, 'Başarıyla çıkış yapıldı.')
    return redirect('kullanicilar:login')


def profile_view(request):
    """User profile page showing user information"""
    if not request.session.get('is_authenticated'):
        messages.error(request, 'Bu sayfayı görüntülemek için giriş yapmalısınız.')
        return redirect('kullanicilar:login')
    
    user_id = request.session.get('user_id')
    
    try:
        kullanici = Kullanici.objects.get(id=user_id)
        
        if request.method == 'POST':
            new_username = request.POST.get('kullanici_adi', '').strip()
            new_isim = request.POST.get('isim', '').strip()
            new_bolum = request.POST.get('bolum', '').strip()
            
            if new_username and new_username != kullanici.kullanici_adi:
                if Kullanici.objects.filter(kullanici_adi=new_username).exclude(id=user_id).exists():
                    messages.error(request, 'Bu kullanıcı adı zaten kullanılıyor.')
                    return redirect('kullanicilar:profile')
                kullanici.kullanici_adi = new_username
                request.session['user_username'] = new_username
            
            if new_isim:
                kullanici.isim = new_isim
                request.session['user_isim'] = new_isim
            
            if new_bolum:
                kullanici.bolum = new_bolum
            
            kullanici.save()
            messages.success(request, 'Profil bilgileriniz başarıyla güncellendi!')
            return redirect('kullanicilar:profile')
        
        context = {
            'kullanici': kullanici,
        }
        return render(request, 'kullanicilar/profile.html', context)
        
    except Kullanici.DoesNotExist:
        messages.error(request, 'Kullanıcı bulunamadı.')
        return redirect('kullanicilar:login')
        