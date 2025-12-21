from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


from django.contrib.auth.models import User


@csrf_exempt  # Postman'dan test ederken CSRF korumasını devre dışı bırakıyoruz
def register_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            
            # Kullanıcı adının benzersiz olduğunu kontrol et
            if User.objects.filter(username=username).exists():
                return JsonResponse({
                    'status': 'error',
                    'message': 'Bu kullanıcı adı zaten kullanılıyor.'
                }, status=400)
                
            # Kullanıcıyı oluştur
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            
            return JsonResponse({
                'status': 'success',
                'message': 'Kullanıcı başarıyla oluşturuldu',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
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
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('index')  # Ana sayfaya yönlendir (index ismindeki URL'e)
            else:
                messages.error(request, 'Geçersiz kullanıcı adı veya şifre.')
        else:
            messages.error(request, 'Lütfen kullanıcı adı ve şifrenizi girin.')
    
    return render(request, 'kullanicilar/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Başarıyla çıkış yapıldı.')
    return redirect('kullanicilar:login')        