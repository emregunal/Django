from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from Kullanıcılar.decorators import kullanici_login_required

@kullanici_login_required
def index(request):
    from Akademik.DevamsizlikTakvimi.models import Devamsizlik
    from Akademik.AkademikTakvim.models import AkademikEtkinlik
    from datetime import datetime, timedelta
    
    ders_istatistikleri = []
    
    
    bugun = datetime.now().date()
    hafta_basi = bugun - timedelta(days=bugun.weekday())
    
    gunler = []
    gun_isimleri = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi', 'Pazar']
    
    for i in range(7):
        gun_tarihi = hafta_basi + timedelta(days=i)
        gun_etkinlikleri = AkademikEtkinlik.objects.filter(tarih=gun_tarihi).order_by('baslangic_saati')
        
        gunler.append({
            'tarih': gun_tarihi,
            'gun_adi': gun_isimleri[i],
            'gun_kisa': gun_isimleri[i][:3],
            'gun_numarasi': gun_tarihi.day,
            'bugun_mu': gun_tarihi == bugun,
            'etkinlikler': gun_etkinlikleri
        })
    
    context = {
        'ders_istatistikleri': ders_istatistikleri[:3],
        'gunler': gunler,
        'hafta_basi': hafta_basi,
    }
    
    return render(request, "index.html", context)