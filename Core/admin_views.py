"""
Admin Panel Views
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from Core.admin_auth import admin_required, superadmin_required, club_moderator_required, authenticate_admin
from Core.mongodb_utils import get_db
from bson import ObjectId
from datetime import datetime

def admin_login(request):
    """Admin login page"""
    if request.session.get('is_admin'):
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        role = authenticate_admin(username, password)
        if role:
            # Update last login time in database
            from Kullanıcılar.models import Kullanici
            try:
                kullanici = Kullanici.objects.get(kullanici_adi=username)
                kullanici.update_last_login()
            except Kullanici.DoesNotExist:
                pass
            
            request.session['is_admin'] = True
            request.session['admin_username'] = username
            request.session['admin_role'] = role
            messages.success(request, f'Hoş geldiniz, {username}!')
            
            # Role'e göre yönlendir
            if role == 'club_moderator':
                return redirect('admin_events')
            else:
                return redirect('admin_dashboard')
        else:
            messages.error(request, 'Kullanıcı adı veya şifre hatalı!')
    
    return render(request, 'admin/login.html')



@superadmin_required
def admin_dashboard(request):
    """Admin dashboard (superadmin only)"""
    db = get_db()
    
    # İstatistikler
    total_appointments = db.randevular.count_documents({})
    pending_appointments = db.randevular.count_documents({'durum': 'bekliyor'})
    approved_appointments = db.randevular.count_documents({'durum': 'onaylandi'})
    rejected_appointments = db.randevular.count_documents({'durum': 'reddedildi'})
    
    # Son bekleyen randevular
    recent_pending = list(db.randevular.find({'durum': 'bekliyor'}).sort('olusturma_tarihi', -1).limit(5))
    
    context = {
        'admin_username': request.session.get('admin_username'),
        'total_appointments': total_appointments,
        'pending_appointments': pending_appointments,
        'approved_appointments': approved_appointments,
        'rejected_appointments': rejected_appointments,
        'recent_pending': recent_pending,
    }
    return render(request, 'admin/dashboard.html', context)

@superadmin_required
def admin_appointments(request):
    """Appointment management"""
    db = get_db()
    
    # Filtreleme
    status_filter = request.GET.get('status', 'bekliyor')
    
    query = {}
    if status_filter and status_filter != 'all':
        query['durum'] = status_filter
    
    appointments_raw = list(db.randevular.find(query).sort('olusturma_tarihi', -1))
    
    # Serialize appointments for template
    appointments = []
    for apt in appointments_raw:
        apt['id'] = str(apt['_id'])
        appointments.append(apt)
    
    context = {
        'admin_username': request.session.get('admin_username'),
        'appointments': appointments,
        'status_filter': status_filter,
    }
    return render(request, 'admin/appointments.html', context)

@admin_required
def approve_appointment(request, appointment_id):
    """Approve appointment"""
    if request.method == 'POST':
        db = get_db()
        
        result = db.randevular.update_one(
            {'_id': ObjectId(appointment_id)},
            {
                '$set': {
                    'durum': 'onaylandi',
                    'onay_tarihi': datetime.now(),
                    'onaylayan': request.session.get('admin_username')
                }
            }
        )
        
        if result.modified_count > 0:
            messages.success(request, 'Randevu başarıyla onaylandı!')
        else:
            messages.error(request, 'Randevu onaylanamadı!')
    
    return redirect('admin_appointments')

@admin_required
def reject_appointment(request, appointment_id):
    """Reject appointment"""
    if request.method == 'POST':
        db = get_db()
        
        result = db.randevular.update_one(
            {'_id': ObjectId(appointment_id)},
            {
                '$set': {
                    'durum': 'reddedildi',
                    'red_tarihi': datetime.now(),
                    'reddeden': request.session.get('admin_username')
                }
            }
        )
        
        if result.modified_count > 0:
            messages.success(request, 'Randevu reddedildi!')
        else:
            messages.error(request, 'Randevu reddedilemedi!')
    
    return redirect('admin_appointments')

@admin_required
def admin_logout(request):
    """Admin logout"""
    # Sadece admin session değerlerini temizle, ana site login'i koru
    if 'is_admin' in request.session:
        del request.session['is_admin']
    if 'admin_username' in request.session:
        del request.session['admin_username']
    if 'admin_role' in request.session:
        del request.session['admin_role']
    
    messages.success(request, 'Admin panelinden başarıyla çıkış yaptınız.')
    return redirect('admin_login')

# ==================== EVENT MANAGEMENT ====================

@club_moderator_required
def admin_events(request):
    """Event management page"""
    db = get_db()
    username = request.session.get('admin_username')
    role = request.session.get('admin_role')
    
    # Filtreleme
    status_filter = request.GET.get('status', 'all')
    
    query = {}
    if status_filter and status_filter != 'all':
        query['durum'] = status_filter
    
    # Kulüp yetkilisi sadece kendi etkinliklerini görür
    if role == 'club_moderator':
        query['olusturan'] = username
    
    events_raw = list(db.etkinlikler.find(query).sort('olusturma_tarihi', -1))
    
    # Serialize events
    events = []
    for event in events_raw:
        event['id'] = str(event['_id'])
        events.append(event)
    
    context = {
        'admin_username': username,
        'admin_role': role,
        'events': events,
        'status_filter': status_filter,
    }
    return render(request, 'admin/events.html', context)

@club_moderator_required
def add_event(request):
    """Add new event"""
    if request.method == 'POST':
        db = get_db()
        username = request.session.get('admin_username')
        role = request.session.get('admin_role')
        
        # Ücret bilgisi
        ucret_tipi = request.POST.get('ucret')
        ucret_tutari = None
        if ucret_tipi == 'paid':
            ucret_str = request.POST.get('ucret_tutari', '').strip()
            ucret_tutari = float(ucret_str) if ucret_str else 0
        
        # Kontenjan
        kontenjan_str = request.POST.get('kontenjan', '').strip()
        kontenjan = int(kontenjan_str) if kontenjan_str else None
        
        event_data = {
            'baslik': request.POST.get('baslik'),
            'aciklama': request.POST.get('aciklama'),
            'kategori': request.POST.get('kategori'),
            'tarih': request.POST.get('tarih'),
            'baslangic_saati': request.POST.get('baslangic_saati'),
            'bitis_saati': request.POST.get('bitis_saati'),
            'konum': request.POST.get('konum'),
            'kontenjan': kontenjan,
            'ucret_tipi': ucret_tipi,
            'ucret_tutari': ucret_tutari,
            'durum': 'onaylandi' if role == 'superadmin' else 'bekliyor',
            'olusturan': username,
            'olusturan_role': role,
            'olusturma_tarihi': datetime.now(),
            'katilimcilar': []
        }
        
        db.etkinlikler.insert_one(event_data)
        messages.success(request, 'Etkinlik başarıyla eklendi!')
        return redirect('admin_events')
    
    context = {
        'admin_username': request.session.get('admin_username'),
        'admin_role': request.session.get('admin_role'),
    }
    return render(request, 'admin/add_event.html', context)

@club_moderator_required
def edit_event(request, event_id):
    """Edit event"""
    db = get_db()
    username = request.session.get('admin_username')
    role = request.session.get('admin_role')
    
    event = db.etkinlikler.find_one({'_id': ObjectId(event_id)})
    
    if not event:
        messages.error(request, 'Etkinlik bulunamadı!')
        return redirect('admin_events')
    
    # Kulüp yetkilisi sadece kendi etkinliğini düzenleyebilir
    if role == 'club_moderator' and event.get('olusturan') != username:
        messages.error(request, 'Bu etkinliği düzenleme yetkiniz yok!')
        return redirect('admin_events')
    
    if request.method == 'POST':
        katilimci_limiti_str = request.POST.get('katilimci_limiti', '').strip()
        
        update_data = {
            'baslik': request.POST.get('baslik'),
            'aciklama': request.POST.get('aciklama'),
            'kategori': request.POST.get('kategori'),
            'tarih': request.POST.get('tarih'),
            'saat': request.POST.get('saat'),
            'konum': request.POST.get('konum'),
            'katilimci_limiti': int(katilimci_limiti_str) if katilimci_limiti_str else None,
        }
        
        db.etkinlikler.update_one(
            {'_id': ObjectId(event_id)},
            {'$set': update_data}
        )
        
        messages.success(request, 'Etkinlik başarıyla güncellendi!')
        return redirect('admin_events')
    
    event['id'] = str(event['_id'])
    context = {
        'admin_username': username,
        'admin_role': role,
        'event': event,
    }
    return render(request, 'admin/edit_event.html', context)

@club_moderator_required
def delete_event(request, event_id):
    """Delete event"""
    if request.method == 'POST':
        db = get_db()
        username = request.session.get('admin_username')
        role = request.session.get('admin_role')
        
        event = db.etkinlikler.find_one({'_id': ObjectId(event_id)})
        
        if not event:
            messages.error(request, 'Etkinlik bulunamadı!')
            return redirect('admin_events')
        
        # Kulüp yetkilisi sadece kendi etkinliğini silebilir
        if role == 'club_moderator' and event.get('olusturan') != username:
            messages.error(request, 'Bu etkinliği silme yetkiniz yok!')
            return redirect('admin_events')
        
        db.etkinlikler.delete_one({'_id': ObjectId(event_id)})
        messages.success(request, 'Etkinlik başarıyla silindi!')
    
    return redirect('admin_events')

@superadmin_required
def approve_event(request, event_id):
    """Approve event (superadmin only)"""
    if request.method == 'POST':
        db = get_db()
        
        result = db.etkinlikler.update_one(
            {'_id': ObjectId(event_id)},
            {
                '$set': {
                    'durum': 'onaylandi',
                    'onay_tarihi': datetime.now(),
                    'onaylayan': request.session.get('admin_username')
                }
            }
        )
        
        if result.modified_count > 0:
            messages.success(request, 'Etkinlik onaylandı!')
        else:
            messages.error(request, 'Etkinlik onaylanamadı!')
    
    return redirect('admin_events')

@superadmin_required
def reject_event(request, event_id):
    """Reject event (superadmin only)"""
    if request.method == 'POST':
        db = get_db()
        
        result = db.etkinlikler.update_one(
            {'_id': ObjectId(event_id)},
            {
                '$set': {
                    'durum': 'reddedildi',
                    'red_tarihi': datetime.now(),
                    'reddeden': request.session.get('admin_username')
                }
            }
        )
        
        if result.modified_count > 0:
            messages.success(request, 'Etkinlik reddedildi!')
        else:
            messages.error(request, 'Etkinlik reddedilemedi!')
    
    return redirect('admin_events')
