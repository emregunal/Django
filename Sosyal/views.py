from django.shortcuts import render, redirect
from Kullanıcılar.decorators import kullanici_login_required
from django.contrib import messages
from Core.mongodb_utils import get_db, serialize_mongo_docs
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

@kullanici_login_required
def etkinlikler(request):
    db = get_db()
    
    # Kategori filtreleme
    kategori = request.GET.get('kategori')
    query = {'durum': 'onaylandi'}  # Sadece onaylanan etkinlikler
    if kategori:
        query['kategori'] = kategori
    
    etkinlik_listesi = list(db.etkinlikler.find(query).sort('tarih', -1))
    etkinlik_listesi = serialize_mongo_docs(etkinlik_listesi)
    
    # Kullanıcı ID'sini al
    user_id = request.session.get('user_id')
    
    # Etkinlik verilerini düzenle
    for etkinlik in etkinlik_listesi:
        # Katılımcıları al
        katilimcilar = etkinlik.get('katilimcilar', [])
        
        # Katılımcı sayısını hesapla
        etkinlik['katilimci_sayisi'] = len(katilimcilar)
        
        # Kullanıcının katılım durumunu kontrol et
        etkinlik['katildi_mi'] = any(k.get('user_id') == user_id for k in katilimcilar)
        
        # Tarih string'ini datetime objesine çevir
        if 'tarih' in etkinlik and isinstance(etkinlik['tarih'], str):
            try:
                etkinlik['tarih'] = datetime.strptime(etkinlik['tarih'], '%Y-%m-%d').date()
            except (ValueError, TypeError):
                etkinlik['tarih'] = None
        
        # Saat string'lerini time objesine çevir
        for saat_field in ['baslangic_saati', 'bitis_saati']:
            if saat_field in etkinlik and isinstance(etkinlik[saat_field], str):
                try:
                    etkinlik[saat_field] = datetime.strptime(etkinlik[saat_field], '%H:%M').time()
                except (ValueError, TypeError):
                    etkinlik[saat_field] = None
    
    context = {
        'etkinlikler': etkinlik_listesi,
    }
    return render(request, 'etkinlikler.html', context)

@kullanici_login_required
def kulupler(request):
    db = get_db()
    
    # Kategori filtreleme
    kategori = request.GET.get('kategori')
    query = {'durum': 'onaylandi'} # Sadece onaylı kulüpleri göster
    if kategori:
        query['kategori'] = kategori
    
    kulup_listesi = list(db.kulupler.find(query).sort('ad', 1))
    kulup_listesi = serialize_mongo_docs(kulup_listesi)
    
    # Kullanıcının katılım durumunu kontrol et
    user_id = request.session.get('user_id')
    for kulup in kulup_listesi:
        uyeler = kulup.get('uyeler', [])
        kulup['katildi_mi'] = any(u.get('user_id') == user_id for u in uyeler)
        kulup['uye_sayisi'] = len(uyeler)
    
    context = {
        'kulupler': kulup_listesi,
    }
    return render(request, 'kulupler.html', context)


@kullanici_login_required
@csrf_exempt
def kulup_katil(request, kulup_id):
    from django.http import JsonResponse
    from bson import ObjectId
    
    if request.method == 'POST':
        db = get_db()
        
        try:
            kulup = db.kulupler.find_one({'_id': ObjectId(kulup_id)})
            
            if not kulup:
                return JsonResponse({'success': False, 'error': 'Kulüp bulunamadı'})
            
            # Kullanıcı bilgilerini session'dan al
            user_id = request.session.get('user_id')
            user_username = request.session.get('user_username')
            
            if not user_id:
                return JsonResponse({'success': False, 'error': 'Giriş yapmalısınız'})
            
            # Üyeler listesini al
            uyeler = kulup.get('uyeler', [])
            
            # Kullanıcı zaten üye mi kontrol et
            uye_mi = any(u.get('user_id') == user_id for u in uyeler)
            
            if uye_mi:
                # Kullanıcı zaten üye, çıkar
                db.kulupler.update_one(
                    {'_id': ObjectId(kulup_id)},
                    {'$pull': {'uyeler': {'user_id': user_id}}}
                )
                katildi = False
                uyeler = [u for u in uyeler if u.get('user_id') != user_id]
            else:
                # Kullanıcıyı ekle
                uye_data = {
                    'user_id': user_id,
                    'username': user_username,
                    'katilim_tarihi': datetime.now()
                }
                db.kulupler.update_one(
                    {'_id': ObjectId(kulup_id)},
                    {'$addToSet': {'uyeler': uye_data}}
                )
                katildi = True
                uyeler.append(uye_data)
            
            return JsonResponse({
                'success': True,
                'katildi': katildi,
                'uye_sayisi': len(uyeler)
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False})

@kullanici_login_required
def duyurular(request):
    db = get_db()
    import re
    
    # Turkish month mapping for date parsing
    turkish_months = {
        'Ocak': 1, 'Şubat': 2, 'Mart': 3, 'Nisan': 4,
        'Mayıs': 5, 'Haziran': 6, 'Temmuz': 7, 'Ağustos': 8,
        'Eylül': 9, 'Ekim': 10, 'Kasım': 11, 'Aralık': 12
    }
    
    def parse_turkish_date(date_str):
        if not date_str:
            return datetime(9999, 12, 31)
        try:
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
        return datetime(9999, 12, 31)
    
    duyuru_listesi = []
    
    # 1. Yaklaşan akademik takvim etkinlikleri
    akademik_etkinlikler = list(db.akademik_etkinlikler.find({'egitim_ogretim_yili': '2025-2026'}))
    bugun = datetime.now()
    for etk in akademik_etkinlikler:
        etk_tarihi = parse_turkish_date(etk.get('tarih'))
        if etk_tarihi >= bugun and etk_tarihi.year != 9999:
            tip_label = {
                'sinav': 'Sınav',
                'tatil': 'Tatil',
                'kayit_basvuru': 'Kayıt/Başvuru',
                'donem': 'Dönem'
            }.get(etk.get('tip'), 'Akademik')
            
            duyuru_listesi.append({
                'id': str(etk.get('_id', '')),
                'baslik': f"Akademik Takvim: {etk.get('baslik', 'Etkinlik')}",
                'icerik': f"{etk.get('aciklama', '')} - Tarih: {etk.get('tarih', 'Belirtilmedi')} - Tür: {tip_label}",
                'kategori': 'akademik',
                'yazar': 'Akademik Takvim',
                'olusturma_tarihi': etk_tarihi,
                'tip': 'akademik'
            })
    
    # 1b. Devamsızlık sınırı uyarıları (kullanıcıya özel)
    user_id = request.session.get('user_id')
    if user_id:
        dersler = list(db.dersler.find({'ogrenci_id': user_id}))
        for ders in dersler:
            toplam_saat = ders.get('toplam_saat', ders.get('haftalik_ders_saati', 3) * 14)
            devamsiz_saat = ders.get('devamsiz_saat', 0)
            devam_zorunlulugu = ders.get('devam_zorunlulugu', 70)
            
            # Kalan hak hesapla
            izin_verilen_devamsizlik = toplam_saat * (100 - devam_zorunlulugu) / 100
            kalan_hak = int(izin_verilen_devamsizlik - devamsiz_saat)
            
            # Sınırı aştıysa veya çok yaklaştıysa uyarı ver
            if kalan_hak <= 0:
                duyuru_listesi.append({
                    'id': str(ders.get('_id', '')),
                    'baslik': f"UYARI: {ders.get('ders_adi', 'Ders')} - Devamsızlık Sınırı Aşıldı!",
                    'icerik': f"Bu derste devamsızlık sınırını aştınız! Toplam {devamsiz_saat} saat devamsızlık yaptınız. Dersten kalıyorsunuz.",
                    'kategori': 'acil',
                    'yazar': 'Devamsızlık Sistemi',
                    'olusturma_tarihi': datetime.now(),
                    'tip': 'devamsizlik_uyari'
                })
            elif kalan_hak <= 3:
                duyuru_listesi.append({
                    'id': str(ders.get('_id', '')),
                    'baslik': f"DİKKAT: {ders.get('ders_adi', 'Ders')} - Devamsızlık Sınırına Yaklaşıyorsunuz!",
                    'icerik': f"Bu derste sadece {kalan_hak} saat devamsızlık hakkınız kaldı! Dikkatli olun.",
                    'kategori': 'acil',
                    'yazar': 'Devamsızlık Sistemi',
                    'olusturma_tarihi': datetime.now(),
                    'tip': 'devamsizlik_uyari'
                })
    
    # 2. Onaylanan etkinlikleri duyuru olarak ekle
    etkinlikler = list(db.etkinlikler.find({'durum': 'onaylandi'}).sort('olusturma_tarihi', -1).limit(10))
    for etkinlik in etkinlikler:
        duyuru_listesi.append({
            'id': str(etkinlik.get('_id', '')),
            'baslik': f"Yeni Etkinlik: {etkinlik.get('baslik', 'Etkinlik')}",
            'icerik': f"{etkinlik.get('aciklama', '')} - Tarih: {etkinlik.get('tarih', 'Belirtilmedi')} - Konum: {etkinlik.get('konum', 'Belirtilmedi')}",
            'kategori': 'sosyal',
            'yazar': etkinlik.get('olusturan', 'Etkinlik Yönetimi'),
            'olusturma_tarihi': etkinlik.get('olusturma_tarihi', datetime.now()),
            'tip': 'etkinlik'
        })
    
    # 3. Onaylanan kulüpleri duyuru olarak ekle
    kulupler = list(db.kulupler.find({'durum': 'onaylandi'}).sort('olusturma_tarihi', -1).limit(10))
    for kulup in kulupler:
        uye_sayisi = len(kulup.get('uyeler', []))
        duyuru_listesi.append({
            'id': str(kulup.get('_id', '')),
            'baslik': f"Kulüp: {kulup.get('ad', 'Kulüp')}",
            'icerik': f"{kulup.get('aciklama', '')} - Kategori: {kulup.get('kategori', 'Genel').title()} - {uye_sayisi} üye",
            'kategori': 'genel',
            'yazar': kulup.get('baskan', 'Kulüp Yönetimi'),
            'olusturma_tarihi': kulup.get('olusturma_tarihi', datetime.now()),
            'tip': 'kulup'
        })
    
    # 4. Varsa duyurular koleksiyonundan da ekle
    duyurular_db = list(db.duyurular.find({}).sort('olusturma_tarihi', -1).limit(10))
    for duyuru in duyurular_db:
        duyuru_listesi.append({
            'id': str(duyuru.get('_id', '')),
            'baslik': duyuru.get('baslik', 'Duyuru'),
            'icerik': duyuru.get('icerik', ''),
            'kategori': duyuru.get('kategori', 'genel'),
            'yazar': duyuru.get('yazar', 'Yönetim'),
            'olusturma_tarihi': duyuru.get('olusturma_tarihi', datetime.now()),
            'tip': 'duyuru'
        })
    
    # Tarihe göre sırala (en yakından en uzağa - akademik için, diğerleri için tarihe göre)
    duyuru_listesi.sort(key=lambda x: x.get('olusturma_tarihi', datetime.now()), reverse=True)
    
    # En yakın 2 akademik etkinliği ayrı listede tut (tarihe göre sıralı)
    akademik_duyurular = [d for d in duyuru_listesi if d.get('tip') == 'akademik']
    akademik_duyurular.sort(key=lambda x: x.get('olusturma_tarihi', datetime.now()))
    yaklasan_akademik = akademik_duyurular[:2]
    
    context = {
        'duyurular': duyuru_listesi,
        'yaklasan_akademik': yaklasan_akademik,
    }
    return render(request, 'duyurular.html', context)

@kullanici_login_required
@csrf_exempt
def etkinlik_katil(request, etkinlik_id):
    from django.http import JsonResponse
    from bson import ObjectId
    
    if request.method == 'POST':
        db = get_db()
        
        try:
            etkinlik = db.etkinlikler.find_one({'_id': ObjectId(etkinlik_id)})
            
            if not etkinlik:
                return JsonResponse({'success': False, 'error': 'Etkinlik bulunamadı'})
            
            # Kullanıcı bilgilerini session'dan al
            user_id = request.session.get('user_id')
            user_username = request.session.get('user_username')
            
            if not user_id:
                return JsonResponse({'success': False, 'error': 'Giriş yapmalısınız'})
            
            # Katılımcılar listesini al
            katilimcilar = etkinlik.get('katilimcilar', [])
            
            # Kullanıcı zaten katılmış mı kontrol et
            katildi_mi = any(k.get('user_id') == user_id for k in katilimcilar)
            
            if katildi_mi:
                # Kullanıcı zaten katılmış, çıkar
                db.etkinlikler.update_one(
                    {'_id': ObjectId(etkinlik_id)},
                    {'$pull': {'katilimcilar': {'user_id': user_id}}}
                )
                katildi = False
                katilimcilar = [k for k in katilimcilar if k.get('user_id') != user_id]
            else:
                # Kullanıcıyı ekle
                katilimci_data = {
                    'user_id': user_id,
                    'username': user_username,
                    'katilim_tarihi': datetime.now()
                }
                db.etkinlikler.update_one(
                    {'_id': ObjectId(etkinlik_id)},
                    {'$addToSet': {'katilimcilar': katilimci_data}}
                )
                katildi = True
                katilimcilar.append(katilimci_data)
            
            return JsonResponse({
                'success': True,
                'katildi': katildi,
                'katilimci_sayisi': len(katilimcilar)
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False})
