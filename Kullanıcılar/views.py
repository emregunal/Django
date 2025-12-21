from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from Kullanıcılar.models import Kullanici
import json


@csrf_exempt  # Postman'dan test ederken CSRF korumasını devre dışı bırakıyoruz
def register_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            
            # Kullanıcı adının benzersiz olduğunu kontrol et
            if Kullanici.objects.filter(kullanici_adi=username).exists():
                return JsonResponse({
                    'status': 'error',
                    'message': 'Bu kullanıcı adı zaten kullanılıyor.'
                }, status=400)
                
            # Kullanıcıyı oluştur
            kullanici = Kullanici(
                kullanici_adi=username,
                email=email,
                rol='user',  # API'den kayıt olan kullanıcılar normal kullanıcı
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
    # Eğer kullanıcı zaten giriş yapmışsa ana sayfaya yönlendir
    if request.session.get('is_authenticated'):
        return redirect('index')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            try:
                # Kullanıcıyı veritabanından bul
                kullanici = Kullanici.objects.get(kullanici_adi=username)
                
                # Şifreyi kontrol et
                if kullanici.check_password(password):
                    # Hesap aktif mi kontrol et
                    if not kullanici.aktif:
                        messages.error(request, 'Hesabınız devre dışı bırakılmış.')
                        return render(request, 'kullanicilar/login.html')
                    
                    # Sadece normal kullanıcıların ana siteye giriş yapmasına izin ver
                    if kullanici.rol != 'user':
                        messages.error(request, 'Bu giriş sayfası sadece normal kullanıcılar içindir. Admin paneli için admin girişini kullanın.')
                        return render(request, 'kullanicilar/login.html')
                    
                    # Session'a kullanıcı bilgilerini kaydet
                    request.session['user_id'] = kullanici.id
                    request.session['user_username'] = kullanici.kullanici_adi
                    request.session['user_role'] = kullanici.rol
                    request.session['user_isim'] = kullanici.isim if kullanici.isim else kullanici.kullanici_adi
                    request.session['is_authenticated'] = True
                    
                    # Son giriş zamanını güncelle
                    kullanici.update_last_login()
                    
                    messages.success(request, f'Hoş geldiniz, {kullanici.kullanici_adi}!')
                    return redirect('index')  # Ana sayfaya yönlendir
                else:
                    messages.error(request, 'Geçersiz kullanıcı adı veya şifre.')
            
            except Kullanici.DoesNotExist:
                messages.error(request, 'Geçersiz kullanıcı adı veya şifre.')
        else:
            messages.error(request, 'Lütfen kullanıcı adı ve şifrenizi girin.')
    
    return render(request, 'kullanicilar/login.html')

def logout_view(request):
    # Session'ı tamamen temizle
    request.session.flush()
    
    messages.success(request, 'Başarıyla çıkış yapıldı.')
    return redirect('kullanicilar:login')
        