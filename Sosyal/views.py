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
    
    # Etkinlik verilerini düzenle
    for etkinlik in etkinlik_listesi:
        # Katılımcı sayısını hesapla
        etkinlik['katilimci_sayisi'] = len(etkinlik.get('katilimcilar', []))
        
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
    query = {}
    if kategori:
        query['kategori'] = kategori
    
    kulup_listesi = list(db.kulupler.find(query).sort('ad', 1))
    kulup_listesi = serialize_mongo_docs(kulup_listesi)
    
    context = {
        'kulupler': kulup_listesi,
    }
    return render(request, 'kulupler.html', context)

@kullanici_login_required
def duyurular(request):
    db = get_db()
    
    # Kategori filtreleme
    kategori = request.GET.get('kategori')
    query = {}
    if kategori:
        query['kategori'] = kategori
    
    duyuru_listesi = list(db.duyurular.find(query).sort('olusturma_tarihi', -1))
    duyuru_listesi = serialize_mongo_docs(duyuru_listesi)
    
    context = {
        'duyurular': duyuru_listesi,
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
