from django.shortcuts import render, redirect
from Kullanıcılar.decorators import kullanici_login_required
from django.contrib import messages
from Core.mongodb_utils import get_db, serialize_mongo_docs
from datetime import datetime
import re

def parse_turkish_date(date_str):
    """
    Parse Turkish date strings and extract the first date for sorting.
    Handles formats like:
    - "15 Eylül 2025"
    - "10-30 Temmuz 2025" (range)
    - "28 (Yarım Gün) - 29 Ekim 2025"
    """
    if not date_str:
        return datetime(9999, 12, 31)  # Put None dates at the end
    
    # Turkish month mapping
    turkish_months = {
        'Ocak': 1, 'Şubat': 2, 'Mart': 3, 'Nisan': 4,
        'Mayıs': 5, 'Haziran': 6, 'Temmuz': 7, 'Ağustos': 8,
        'Eylül': 9, 'Ekim': 10, 'Kasım': 11, 'Aralık': 12
    }
    
    try:
        # Extract first number, month name, and year
        # Match patterns like "15 Eylül 2025" or "10-30 Temmuz 2025"
        match = re.search(r'(\d+).*?([A-ZÇĞİÖŞÜ][a-zçğıöşü]+)\s+(\d{4})', date_str)
        if match:
            day = int(match.group(1))
            month_name = match.group(2)
            year = int(match.group(3))
            
            month = turkish_months.get(month_name)
            if month:
                return datetime(year, month, day)
    except:
        pass
    
    return datetime(9999, 12, 31)  # If parsing fails, put at the end

@kullanici_login_required
def akademik_takvim(request):
    db = get_db()
    
    # Tüm akademik etkinlikleri getir
    etkinlikler = list(db.akademik_etkinlikler.find({'egitim_ogretim_yili': '2025-2026'}))
    
    # Kategorilere göre ayır
    sinavlar = []
    tatiller = []
    kayit_basvurular = []
    donem_tarihleri = []
    
    for etk in etkinlikler:
        etkinlik_obj = {
            'baslik': etk.get('baslik'),
            'aciklama': etk.get('aciklama'),
            'tarih': etk.get('tarih'),
            'tip': etk.get('tip'),
            'kategori': etk.get('kategori'),
            'donem': etk.get('donem'),
            'konum': etk.get('konum')
        }
        
        if etk.get('tip') == 'sinav':
            sinavlar.append(etkinlik_obj)
        elif etk.get('tip') == 'tatil':
            tatiller.append(etkinlik_obj)
        elif etk.get('tip') == 'kayit_basvuru':
            kayit_basvurular.append(etkinlik_obj)
        elif etk.get('tip') == 'donem':
            donem_tarihleri.append(etkinlik_obj)
    
    # Tarihe göre sırala
    sinavlar.sort(key=lambda x: parse_turkish_date(x.get('tarih')))
    tatiller.sort(key=lambda x: parse_turkish_date(x.get('tarih')))
    kayit_basvurular.sort(key=lambda x: parse_turkish_date(x.get('tarih')))
    donem_tarihleri.sort(key=lambda x: parse_turkish_date(x.get('tarih')))
    
    # Diğer önemli tarihler (kayıt + dönem)
    diger = kayit_basvurular + donem_tarihleri
    diger.sort(key=lambda x: parse_turkish_date(x.get('tarih')))
    
    # Yaklaşan etkinlikler - tüm etkinlikleri birleştir ve tarihe göre sırala
    tum_etkinlikler = sinavlar + tatiller + diger
    tum_etkinlikler.sort(key=lambda x: parse_turkish_date(x.get('tarih')))
    
    # Bugünden sonraki ilk 10 etkinliği al
    yaklasan = []
    bugun = datetime.now()
    for etk in tum_etkinlikler:
        etk_tarihi = parse_turkish_date(etk.get('tarih'))
        if etk_tarihi >= bugun:
            yaklasan.append(etk)
            if len(yaklasan) >= 10:
                break
    
    context = {
        'sinavlar': sinavlar,
        'tatiller': tatiller,
        'diger': diger,
        'yaklasan_etkinlikler': yaklasan,
    }
    return render(request, 'canliAkademikTakvim.html', context)

@kullanici_login_required
def canliAkademikTakvim(request):
    return akademik_takvim(request)

