from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from Sosyal.models import Kulup
from django.contrib import messages

@login_required(login_url='/Kullanıcılar/login/')
def kulupOner(request):
    if request.method == 'POST':
        ad = request.POST.get('ad')
        kategori = request.POST.get('kategori')
        aciklama = request.POST.get('aciklama')
        
        try:
            Kulup.objects.create(
                ad=ad,
                kategori=kategori,
                aciklama=aciklama,
                kurucu=request.user
            )
            messages.success(request, 'Kulüp öneriniz başarıyla gönderildi!')
            return redirect('kulupler')
        except Exception as e:
            messages.error(request, 'Kulüp oluşturulurken bir hata oluştu.')
    
    return render(request, "kulupOner.html")
