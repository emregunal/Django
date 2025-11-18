from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Etkinlik, Kulup, Duyuru
from django.contrib import messages


@login_required(login_url='/Kullanıcılar/login/')
def etkinlikler(request):
    etkinlik_listesi = Etkinlik.objects.all().order_by('-tarih')
    
    # Kategori filtreleme
    kategori = request.GET.get('kategori')
    if kategori:
        etkinlik_listesi = etkinlik_listesi.filter(kategori=kategori)
    
    context = {
        'etkinlikler': etkinlik_listesi,
    }
    return render(request, 'etkinlikler.html', context)

@login_required(login_url='/Kullanıcılar/login/')
def kulupler(request):
    kulup_listesi = Kulup.objects.all()
    
    # Kategori filtreleme
    kategori = request.GET.get('kategori')
    if kategori:
        kulup_listesi = kulup_listesi.filter(kategori=kategori)
    
    context = {
        'kulupler': kulup_listesi,
    }
    return render(request, 'kulupler.html', context)

@login_required(login_url='/Kullanıcılar/login/')
def duyurular(request):
    duyuru_listesi = Duyuru.objects.all().order_by('-olusturma_tarihi')
    
    # Kategori filtreleme
    kategori = request.GET.get('kategori')
    if kategori:
        duyuru_listesi = duyuru_listesi.filter(kategori=kategori)
    
    context = {
        'duyurular': duyuru_listesi,
    }
    return render(request, 'duyurular.html', context)

# Etkinliğe katıl/ayrıl AJAX endpoint
@login_required(login_url='/Kullanıcılar/login/')
def etkinlik_katil(request, etkinlik_id):
    if request.method == 'POST':
        etkinlik = get_object_or_404(Etkinlik, id=etkinlik_id)
        
        if request.user in etkinlik.katilimcilar.all():
            etkinlik.katilimcilar.remove(request.user)
            katildi = False
        else:
            etkinlik.katilimcilar.add(request.user)
            katildi = True
        
        return JsonResponse({
            'success': True,
            'katildi': katildi,
            'katilimci_sayisi': etkinlik.katilimci_sayisi()
        })
    
    return JsonResponse({'success': False})
