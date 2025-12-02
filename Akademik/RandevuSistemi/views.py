from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Ogretmen, Randevu
from django.contrib import messages


@login_required(login_url='/Kullanıcılar/login/')
def randevuSistemi(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        # Randevu talebi oluşturma
        if action == 'create':
            ogretmen_id = request.POST.get('ogretmen')
            tarih = request.POST.get('tarih')
            baslangic_saati = request.POST.get('baslangic_saati')
            bitis_saati = request.POST.get('bitis_saati')
            konu = request.POST.get('konu')
            aciklama = request.POST.get('aciklama', '')
            
            try:
                ogretmen = Ogretmen.objects.get(id=ogretmen_id)
                Randevu.objects.create(
                    ogrenci=request.user,
                    ogretmen=ogretmen,
                    tarih=tarih,
                    baslangic_saati=baslangic_saati,
                    bitis_saati=bitis_saati,
                    konu=konu,
                    aciklama=aciklama,
                    durum='bekliyor'
                )
                messages.success(request, 'Randevu talebiniz oluşturuldu! Onay bekleniyor.')
            except Ogretmen.DoesNotExist:
                messages.error(request, 'Öğretmen bulunamadı!')
            except Exception as e:
                messages.error(request, f'Randevu oluşturulurken hata: {str(e)}')
        
        # Randevu iptal etme
        elif action == 'cancel':
            randevu_id = request.POST.get('randevu_id')
            try:
                randevu = Randevu.objects.get(id=randevu_id, ogrenci=request.user)
                randevu.durum = 'iptal'
                randevu.save()
                messages.success(request, 'Randevu iptal edildi.')
            except Randevu.DoesNotExist:
                messages.error(request, 'Randevu bulunamadı!')
        
        # Reddedilen randevuyu geçmişe taşıma
        elif action == 'archive':
            randevu_id = request.POST.get('randevu_id')
            try:
                randevu = Randevu.objects.get(id=randevu_id, ogrenci=request.user, durum='reddedildi')
                randevu.durum = 'iptal'
                randevu.save()
                messages.success(request, 'Randevu geçmiş randevulara taşındı.')
            except Randevu.DoesNotExist:
                messages.error(request, 'Randevu bulunamadı veya reddedilmiş değil!')
        
        return redirect('randevu-sistemi')
    
    from datetime import date
    
    # Kullanıcının randevularını getir
    randevular = Randevu.objects.filter(ogrenci=request.user).select_related('ogretmen__kullanici').order_by('-tarih')
    
    # Aktif ve geçmiş randevuları ayır
    bugun = date.today()
    aktif_randevular = randevular.filter(tarih__gte=bugun).exclude(durum='iptal')
    gecmis_randevular = randevular.filter(tarih__lt=bugun) | randevular.filter(durum='iptal')
    
    ogretmenler = Ogretmen.objects.all().select_related('kullanici')
    
    context = {
        'aktif_randevular': aktif_randevular,
        'gecmis_randevular': gecmis_randevular,
        'ogretmenler': ogretmenler,
    }
    return render(request,"randevuSistemi.html", context)


@staff_member_required
def randevuYonetim(request):
    """Admin için randevu onay/red sayfası"""
    if request.method == 'POST':
        randevu_id = request.POST.get('randevu_id')
        action = request.POST.get('action')
        
        try:
            randevu = Randevu.objects.get(id=randevu_id)
            if action == 'onayla':
                randevu.durum = 'onaylandi'
                randevu.save()
                messages.success(request, f'{randevu.ogrenci.username} kullanıcısının randevusu onaylandı.')
            elif action == 'reddet':
                randevu.durum = 'reddedildi'
                randevu.save()
                messages.warning(request, f'{randevu.ogrenci.username} kullanıcısının randevusu reddedildi.')
        except Randevu.DoesNotExist:
            messages.error(request, 'Randevu bulunamadı!')
        
        return redirect('randevu-yonetim')
    
    # Tüm randevuları getir
    tum_randevular = Randevu.objects.all().select_related('ogrenci', 'ogretmen__kullanici').order_by('-tarih')
    bekleyen_randevular = tum_randevular.filter(durum='bekliyor')
    
    context = {
        'bekleyen_randevular': bekleyen_randevular,
        'tum_randevular': tum_randevular,
    }
    return render(request, 'randevuYonetim.html', context)
