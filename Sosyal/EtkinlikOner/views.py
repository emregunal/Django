from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from Sosyal.models import Etkinlik
from django.contrib import messages

@login_required(login_url='/Kullanıcılar/login/')
def etkinlikOner(request):
    if request.method == 'POST':
        baslik = request.POST.get('baslik')
        kategori = request.POST.get('kategori')
        tarih = request.POST.get('tarih')
        baslangic_saati = request.POST.get('baslangic_saati')
        bitis_saati = request.POST.get('bitis_saati')
        konum = request.POST.get('konum')
        aciklama = request.POST.get('aciklama')
        
        try:
            Etkinlik.objects.create(
                baslik=baslik,
                kategori=kategori,
                tarih=tarih,
                baslangic_saati=baslangic_saati,
                bitis_saati=bitis_saati,
                konum=konum,
                aciklama=aciklama,
                olusturan=request.user
            )
            messages.success(request, 'Etkinlik öneriniz başarıyla gönderildi!')
            return redirect('etkinlikler')
        except Exception as e:
            messages.error(request, 'Etkinlik oluşturulurken bir hata oluştu.')
    
    return render(request, "etkinlikOner.html") 
