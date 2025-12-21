from django.shortcuts import render, redirect
from Kullanıcılar.decorators import kullanici_login_required
from django.contrib import messages
from Core.mongodb_utils import get_db, serialize_mongo_docs
from datetime import datetime
from bson import ObjectId

@kullanici_login_required
def randevu_listesi(request):
    db = get_db()
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create':
            # Yeni randevu oluştur
            ogretmen_id = request.POST.get('ogretmen')
            tarih = request.POST.get('tarih')
            baslangic_saati = request.POST.get('baslangic_saati')
            bitis_saati = request.POST.get('bitis_saati')
            konu = request.POST.get('konu')
            aciklama = request.POST.get('aciklama', '')
            
            # Öğretmen bilgisini MongoDB'den al
            ogretmen = db.ogretmenler.find_one({'_id': ObjectId(ogretmen_id)})
            
            if ogretmen:
                # Öğrenci adını session'dan veya kullanıcı adından al
                ogrenci_adi = request.session.get('user_isim', request.session.get('user_username', 'Bilinmeyen'))
                
                db.randevular.insert_one({
                    'ogrenci_id': request.session.get('user_id'),
                    'ogrenci_username': request.session.get('user_username'),
                    'ogrenci_adi': ogrenci_adi,
                    'ogretmen_id': str(ogretmen['_id']),
                    'ogretmen_adi': ogretmen.get('ad'),
                    'ogretmen_unvan': ogretmen.get('unvan'),
                    'ogretmen_bolum': ogretmen.get('bolum'),
                    'ogretmen_ofis': ogretmen.get('ofis'),
                    'tarih': tarih,
                    'baslangic_saati': baslangic_saati,
                    'bitis_saati': bitis_saati,
                    'konu': konu,
                    'aciklama': aciklama,
                    'durum': 'bekliyor',
                    'olusturma_tarihi': datetime.now()
                })
                messages.success(request, 'Randevu talebiniz oluşturuldu!')
            else:
                messages.error(request, 'Öğretmen bulunamadı!')
            return redirect('randevu-sistemi')
            
        elif action == 'cancel':
            # Randevuyu iptal et
            randevu_id = request.POST.get('randevu_id')
            db.randevular.update_one(
                {'_id': ObjectId(randevu_id)},
                {'$set': {'durum': 'iptal'}}
            )
            messages.success(request, 'Randevu iptal edildi!')
            return redirect('randevu-sistemi')
            
        elif action == 'archive':
            # Randevuyu arşivle
            randevu_id = request.POST.get('randevu_id')
            db.randevular.update_one(
                {'_id': ObjectId(randevu_id)},
                {'$set': {'arsivlendi': True}}
            )
            messages.success(request, 'Randevu arşivlendi!')
            return redirect('randevu-sistemi')
    
    # Öğrencinin randevularını getir
    randevular = list(db.randevular.find({'ogrenci_id': request.session.get('user_id')}))
    randevular = serialize_mongo_docs(randevular)
    
    # Aktif ve geçmiş randevuları ayır
    aktif_randevular = []
    gecmis_randevular = []
    
    for randevu in randevular:
        # Randevu objesi oluştur (template için)
        randevu_obj = {
            'id': randevu['id'],
            'ogretmen': {
                'unvan': randevu.get('ogretmen_unvan', ''),
                'kullanici': {
                    'get_full_name': lambda: randevu.get('ogretmen_adi', '')
                },
                'ofis': randevu.get('ogretmen_ofis', '')
            },
            'tarih': randevu.get('tarih'),
            'baslangic_saati': randevu.get('baslangic_saati'),
            'bitis_saati': randevu.get('bitis_saati'),
            'konu': randevu.get('konu'),
            'aciklama': randevu.get('aciklama'),
            'durum': randevu.get('durum', 'bekliyor')
        }
        
        if randevu.get('durum') in ['bekliyor', 'onaylandi', 'reddedildi'] and not randevu.get('arsivlendi'):
            aktif_randevular.append(randevu_obj)
        else:
            gecmis_randevular.append(randevu_obj)
    
    # Tüm öğretmenleri getir
    ogretmenler_list = list(db.ogretmenler.find({'aktif': True}).sort('ad', 1))
    ogretmenler = []
    for ogr in ogretmenler_list:
        ogretmenler.append({
            'id': str(ogr['_id']),
            'unvan': ogr.get('unvan', ''),
            'kullanici': {
                'get_full_name': lambda ad=ogr.get('ad'): ad
            },
            'ad': ogr.get('ad'),
            'bolum': ogr.get('bolum'),
            'ofis': ogr.get('ofis')
        })
    
    context = {
        'aktif_randevular': aktif_randevular,
        'gecmis_randevular': gecmis_randevular,
        'ogretmenler': ogretmenler,
    }
    return render(request, 'randevuSistemi.html', context)

@kullanici_login_required
def randevuSistemi(request):
    return randevu_listesi(request)

@kullanici_login_required
def randevuYonetim(request):
    return randevu_listesi(request)

@kullanici_login_required
def randevu_olustur(request):
    if request.method == 'POST':
        ogretmen_adi = request.POST.get('ogretmen_adi')
        tarih = request.POST.get('tarih')
        baslangic_saati = request.POST.get('baslangic_saati')
        bitis_saati = request.POST.get('bitis_saati')
        konu = request.POST.get('konu')
        aciklama = request.POST.get('aciklama', '')
        
        try:
            db = get_db()
            db.randevular.insert_one({
                'ogrenci_id': request.session.get('user_id'),
                'ogrenci_username': request.session.get('user_username'),
                'ogretmen_adi': ogretmen_adi,
                'tarih': tarih,
                'baslangic_saati': baslangic_saati,
                'bitis_saati': bitis_saati,
                'konu': konu,
                'aciklama': aciklama,
                'durum': 'bekliyor',
                'olusturma_tarihi': datetime.now()
            })
            messages.success(request, 'Randevu talebiniz oluşturuldu!')
            return redirect('randevu_listesi')
        except Exception as e:
            messages.error(request, f'Hata oluştu: {str(e)}')
    
    return render(request, 'randevu_olustur.html')
