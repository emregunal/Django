from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Ogretmen, Randevu
from django.contrib import messages


@login_required(login_url='/Kullanıcılar/login/')
def randevuSistemi(request):
    if request.method == 'POST':
        ogretmen_id = request.POST.get('ogretmen')
        tarih = request.POST.get('tarih')
        baslangic_saati = request.POST.get('baslangic_saati')
        bitis_saati = request.POST.get('bitis_saati')
        konu = request.POST.get('konu')
        aciklama = request.POST.get('aciklama')
        
        try:
            ogretmen = Ogretmen.objects.get(id=ogretmen_id)
            Randevu.objects.create(
                ogrenci=request.user,
                ogretmen=ogretmen,
                tarih=tarih,
                baslangic_saati=baslangic_saati,
                bitis_saati=bitis_saati,
                konu=konu,
                aciklama=aciklama
            )
            messages.success(request, 'Randevu talebiniz başarıyla oluşturuldu!')
            return redirect('randevu-sistemi')
        except Exception as e:
            messages.error(request, 'Randevu oluşturulurken bir hata oluştu.')
    
    # Kullanıcının randevularını getir
    randevular = Randevu.objects.filter(ogrenci=request.user).order_by('-tarih')
    ogretmenler = Ogretmen.objects.all()
    
    context = {
        'randevular': randevular,
        'ogretmenler': ogretmenler,
    }
    return render(request,"randevuSistemi.html", context)
