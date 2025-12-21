from django.shortcuts import render
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import AkademikEtkinlik
from datetime import datetime, timedelta


@login_required(login_url='/Kullanıcılar/login/')
def canliAkademikTakvim(request):
    bugun = datetime.now().date()
    
    # Tüm etkinlikleri getir (geçmiş ve gelecek)
    tum_etkinlikler = AkademikEtkinlik.objects.all()
    
    # Yaklaşan etkinlikler (bugünden itibaren 60 gün)
    yaklasan_etkinlikler = AkademikEtkinlik.objects.filter(
        tarih__gte=bugun,
        tarih__lte=bugun + timedelta(days=60)
    ).order_by('tarih')[:10]
    
    # Etkinlikleri tiplere göre grupla
    sinavlar = tum_etkinlikler.filter(tip='sinav')
    tatiller = tum_etkinlikler.filter(tip='tatil')
    diger = tum_etkinlikler.exclude(tip__in=['sinav', 'tatil'])
    
    context = {
        'etkinlikler': tum_etkinlikler,
        'yaklasan_etkinlikler': yaklasan_etkinlikler,
        'sinavlar': sinavlar,
        'tatiller': tatiller,
        'diger': diger,
        'bugun': bugun,
    }
    return render(request, "canliAkademikTakvim.html", context)

