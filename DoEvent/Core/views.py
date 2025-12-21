from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required(login_url='kullanicilar:login')
def index(request):
    from Akademik.DevamsizlikTakvimi.models import Devamsizlik
    from Akademik.AkademikTakvim.models import AkademikEtkinlik
    from datetime import datetime, timedelta
    
    # Kullanıcının devamsızlık kayıtlarını getir, devam yüzdesine göre sırala (düşükten yükseğe)
    devamsizliklar = Devamsizlik.objects.filter(ogrenci=request.user).select_related('ders')
    
    ders_istatistikleri = []
    for devamsizlik in devamsizliklar:
        ders = devamsizlik.ders
        toplam_saat = ders.toplam_ders_saati()
        devam_yuzdesi = devamsizlik.devamsizlik_yuzdesi()
        kalan_hak = devamsizlik.kalan_devamsizlik_hakki()
        
        ders_istatistikleri.append({
            'ders': ders,
            'devamsiz_saat': devamsizlik.devamsiz_saat,
            'toplam_saat': toplam_saat,
            'devam_yuzdesi': devam_yuzdesi,
            'kalan_hak': kalan_hak,
            'devam_zorunlulugu': ders.devam_zorunlulugu,
        })
    
    # Devam yüzdesine göre sırala (düşükten yükseğe)
    ders_istatistikleri.sort(key=lambda x: x['devam_yuzdesi'])
    
    # Haftalık akademik takvim verileri (bu hafta - Pazartesi'den Pazar'a)
    bugun = datetime.now().date()
    hafta_basi = bugun - timedelta(days=bugun.weekday())  # Pazartesi
    
    # Her gün için etkinlikleri hazırla
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
        'ders_istatistikleri': ders_istatistikleri[:3],  # İlk 3 dersi göster
        'gunler': gunler,
        'hafta_basi': hafta_basi,
    }
    
    return render(request, "index.html", context)