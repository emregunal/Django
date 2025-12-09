from django.shortcuts import render, redirect
from Kullanıcılar.decorators import kullanici_login_required
from django.contrib import messages
from Core.mongodb_utils import get_db, serialize_mongo_docs
from datetime import datetime
from bson import ObjectId

@kullanici_login_required
def devamsizlik_listesi(request):
    db = get_db()
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add_ders':
            # Yeni ders ekle
            ders_adi = request.POST.get('ders_adi')
            devam_zorunlulugu = int(request.POST.get('devam_zorunlulugu', 70))
            haftalik_ders_saati = int(request.POST.get('haftalik_ders_saati', 3))
            
            db.dersler.insert_one({
                'ogrenci_id': request.session.get('user_id'),
                'ogrenci_username': request.session.get('user_username'),
                'ders_adi': ders_adi.upper(),
                'ders_kodu': ders_adi.upper(),
                'devam_zorunlulugu': devam_zorunlulugu,
                'haftalik_ders_saati': haftalik_ders_saati,
                'toplam_saat': haftalik_ders_saati * 14,  # 14 hafta
                'devamsiz_saat': 0,
                'olusturma_tarihi': datetime.now()
            })
            messages.success(request, f'{ders_adi} dersi eklendi!')
            return redirect('devamsizlikTakvimi')
            
        elif action == 'add_devamsizlik':
            # Devamsızlık ekle/çıkar
            ders_id = request.POST.get('ders_id')
            devamsiz_saat = int(request.POST.get('devamsiz_saat', 0))
            
            ders = db.dersler.find_one({'_id': ObjectId(ders_id)})
            if ders:
                yeni_devamsiz = max(0, ders.get('devamsiz_saat', 0) + devamsiz_saat)
                db.dersler.update_one(
                    {'_id': ObjectId(ders_id)},
                    {'$set': {'devamsiz_saat': yeni_devamsiz}}
                )
                if devamsiz_saat > 0:
                    messages.success(request, f'{devamsiz_saat} saat devamsızlık eklendi!')
                else:
                    messages.success(request, f'{abs(devamsiz_saat)} saat devamsızlık çıkarıldı!')
            return redirect('devamsizlikTakvimi')
            
        elif action == 'delete_ders':
            # Ders sil
            ders_id = request.POST.get('ders_id')
            db.dersler.delete_one({'_id': ObjectId(ders_id)})
            messages.success(request, 'Ders silindi!')
            return redirect('devamsizlikTakvimi')
    
    # Öğrencinin derslerini getir
    dersler = list(db.dersler.find({'ogrenci_id': request.session.get('user_id')}))
    
    # İstatistikleri hesapla
    ders_istatistikleri = []
    for ders in dersler:
        toplam_saat = ders.get('toplam_saat', ders.get('haftalik_ders_saati', 3) * 14)
        devamsiz_saat = ders.get('devamsiz_saat', 0)
        katilim_saati = toplam_saat - devamsiz_saat
        devam_yuzdesi = round((katilim_saati / toplam_saat) * 100, 1) if toplam_saat > 0 else 100
        devam_zorunlulugu = ders.get('devam_zorunlulugu', 70)
        
        # Kalan hak hesapla
        izin_verilen_devamsizlik = toplam_saat * (100 - devam_zorunlulugu) / 100
        kalan_hak = max(0, int(izin_verilen_devamsizlik - devamsiz_saat))
        
        ders_istatistikleri.append({
            'ders': {
                'id': str(ders['_id']),
                'ders_adi': ders.get('ders_adi'),
                'ders_kodu': ders.get('ders_kodu'),
                'haftalik_ders_saati': ders.get('haftalik_ders_saati', 3)
            },
            'toplam_saat': toplam_saat,
            'devamsiz_saat': devamsiz_saat,
            'katilim_saati': katilim_saati,
            'devam_yuzdesi': devam_yuzdesi,
            'devam_zorunlulugu': devam_zorunlulugu,
            'kalan_hak': kalan_hak
        })
    
    context = {
        'ders_istatistikleri': ders_istatistikleri,
    }
    return render(request, 'devamsizlikTakvimi.html', context)

@kullanici_login_required
def devamsizlikTakvimi(request):
    return devamsizlik_listesi(request)

@kullanici_login_required
def devamsizlik_ekle(request):
    if request.method == 'POST':
        ders_kodu = request.POST.get('ders_kodu')
        ders_adi = request.POST.get('ders_adi')
        devamsiz_saat = int(request.POST.get('devamsiz_saat', 0))
        aciklama = request.POST.get('aciklama', '')
        
        try:
            db = get_db()
            
            # Aynı ders için kayıt var mı kontrol et
            existing = db.devamsizliklar.find_one({
                'ogrenci_id': request.session.get('user_id'),
                'ders_kodu': ders_kodu
            })
            
            if existing:
                # Güncelle
                db.devamsizliklar.update_one(
                    {'_id': existing['_id']},
                    {
                        '$set': {
                            'devamsiz_saat': devamsiz_saat,
                            'aciklama': aciklama,
                            'guncelleme_tarihi': datetime.now()
                        }
                    }
                )
                messages.success(request, 'Devamsızlık kaydı güncellendi!')
            else:
                # Yeni kayıt
                db.devamsizliklar.insert_one({
                    'ogrenci_id': request.session.get('user_id'),
                    'ogrenci_username': request.session.get('user_username'),
                    'ders_kodu': ders_kodu,
                    'ders_adi': ders_adi,
                    'devamsiz_saat': devamsiz_saat,
                    'aciklama': aciklama,
                    'olusturma_tarihi': datetime.now()
                })
                messages.success(request, 'Devamsızlık kaydı eklendi!')
            
            return redirect('devamsizlik_listesi')
        except Exception as e:
            messages.error(request, f'Hata oluştu: {str(e)}')
    
    return render(request, 'devamsizlik_ekle.html')