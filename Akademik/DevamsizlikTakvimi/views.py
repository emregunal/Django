from django.shortcuts import render
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Ders, Devamsizlik
from django.db.models import Count

@login_required(login_url='/Kullanıcılar/login/')
def devamsizlikTakvimi(request):
    # Kullanıcının derslerini ve devamsızlıklarını getir
    dersler = Ders.objects.all()
    
    ders_istatistikleri = []
    for ders in dersler:
        toplam_devamsizlik = Devamsizlik.objects.filter(
            ogrenci=request.user,
            ders=ders
        ).count()
        
        mazeretli_devamsizlik = Devamsizlik.objects.filter(
            ogrenci=request.user,
            ders=ders,
            mazeret=True
        ).count()
        
        mazaretsiz_devamsizlik = toplam_devamsizlik - mazeretli_devamsizlik
        
        # 14 hafta varsayımıyla devamsızlık yüzdesi
        devamsizlik_yuzdesi = (mazaretsiz_devamsizlik / 14) * 100 if 14 > 0 else 0
        
        ders_istatistikleri.append({
            'ders': ders,
            'toplam_devamsizlik': toplam_devamsizlik,
            'mazeretli': mazeretli_devamsizlik,
            'mazaretsiz': mazaretsiz_devamsizlik,
            'yuzde': round(devamsizlik_yuzdesi, 1),
        })
    
    context = {
        'ders_istatistikleri': ders_istatistikleri,
    }
    return render(request,"devamsizlikTakvimi.html", context)