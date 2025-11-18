from django.shortcuts import render, redirect
from django.http.response import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Ders, Devamsizlik
from django.db.models import Count
from django.contrib import messages

@login_required(login_url='/Kullanıcılar/login/')
def devamsizlikTakvimi(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        # Yeni ders ekleme
        if action == 'add_ders':
            ders_adi = request.POST.get('ders_adi')
            devam_zorunlulugu = request.POST.get('devam_zorunlulugu')
            haftalik_ders_saati = request.POST.get('haftalik_ders_saati')
            
            try:
                # Ders oluştur
                ders, created = Ders.objects.get_or_create(
                    ders_adi=ders_adi,
                    defaults={
                        'ders_kodu': ders_adi.split('(')[1].replace(')', '') if '(' in ders_adi else ders_adi[:10].upper(),
                        'ogretmen': 'Belirtilmedi',
                        'haftalik_ders_saati': int(haftalik_ders_saati),
                        'devam_zorunlulugu': int(devam_zorunlulugu)
                    }
                )
                
                # Devamsızlık kaydı oluştur (0 saat ile başla)
                Devamsizlik.objects.get_or_create(
                    ogrenci=request.user,
                    ders=ders,
                    defaults={'devamsiz_saat': 0}
                )
                
                messages.success(request, f'{ders_adi} dersi başarıyla eklendi!')
            except Exception as e:
                messages.error(request, f'Hata oluştu: {str(e)}')
        
        # Devamsızlık ekleme/azaltma
        elif action == 'add_devamsizlik':
            ders_id = request.POST.get('ders_id')
            devamsiz_saat = int(request.POST.get('devamsiz_saat', 0))
            
            try:
                devamsizlik = Devamsizlik.objects.get(ogrenci=request.user, ders_id=ders_id)
                devamsizlik.devamsiz_saat += devamsiz_saat
                devamsizlik.devamsiz_saat = max(0, devamsizlik.devamsiz_saat)  # Negatif olmasın
                devamsizlik.save()
                messages.success(request, f'{devamsiz_saat} saat devamsızlık eklendi!')
            except Devamsizlik.DoesNotExist:
                messages.error(request, 'Devamsızlık kaydı bulunamadı!')
        
        # Ders silme
        elif action == 'delete_ders':
            ders_id = request.POST.get('ders_id')
            
            try:
                devamsizlik = Devamsizlik.objects.get(ogrenci=request.user, ders_id=ders_id)
                ders_adi = devamsizlik.ders.ders_adi
                devamsizlik.delete()
                messages.success(request, f'{ders_adi} dersi başarıyla silindi!')
            except Devamsizlik.DoesNotExist:
                messages.error(request, 'Ders kaydı bulunamadı!')
        
        return redirect('devamsizlikTakvimi')
    
    # Kullanıcının devamsızlık kayıtlarını getir
    devamsizliklar = Devamsizlik.objects.filter(ogrenci=request.user).select_related('ders')
    
    ders_istatistikleri = []
    for devamsizlik in devamsizliklar:
        ders = devamsizlik.ders
        toplam_saat = ders.toplam_ders_saati()
        devam_yuzdesi = devamsizlik.devamsizlik_yuzdesi()
        kalan_hak = devamsizlik.kalan_devamsizlik_hakki()
        katilim_saati = toplam_saat - devamsizlik.devamsiz_saat
        
        ders_istatistikleri.append({
            'ders': ders,
            'devamsiz_saat': devamsizlik.devamsiz_saat,
            'toplam_saat': toplam_saat,
            'katilim_saati': katilim_saati,
            'devam_yuzdesi': devam_yuzdesi,
            'kalan_hak': kalan_hak,
            'devam_zorunlulugu': ders.devam_zorunlulugu,
        })
    
    context = {
        'ders_istatistikleri': ders_istatistikleri,
    }
    return render(request,"devamsizlikTakvimi.html", context)