"""
Admin Panel Views
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from Core.admin_auth import admin_required, superadmin_required, club_moderator_required, instructor_required, authenticate_admin
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
            elif role in ['instructor', 'ogretmen']:
                return redirect('instructor_appointments')
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
    
    # Filtreleme Parametreleri
    status_filter = request.GET.get('status', 'bekliyor')
    instructor_filter = request.GET.get('instructor', 'all')
    
    query = {}
    if status_filter and status_filter != 'all':
        query['durum'] = status_filter
    
    if instructor_filter and instructor_filter != 'all':
        query['ogretmen_adi'] = instructor_filter
    
    # Randevuları Çek
    appointments_raw = list(db.randevular.find(query).sort('olusturma_tarihi', -1))
    
    # Serialize appointments for template
    appointments = []
    for apt in appointments_raw:
        apt['id'] = str(apt['_id'])
        appointments.append(apt)
        
    # Benzersiz Öğretmen Listesini Çek (Filtreleme Menüsü İçin)
    # Randevulardaki öğretmen isimleri 'ogretmenler' koleksiyonundan geliyor.
    instructors_raw = db.ogretmenler.find({'aktif': True}, {'ad': 1}).sort('ad', 1)
    instructors = []
    for inst in instructors_raw:
        ad = inst.get('ad')
        if ad:
            instructors.append(ad)
    
    context = {
        'admin_username': request.session.get('admin_username'),
        'admin_role': request.session.get('admin_role'),
        'appointments': appointments,
        'status_filter': status_filter,
        'instructor_filter': instructor_filter,
        'instructors': instructors,
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

# ==================== INSTRUCTOR APPOINTMENT MANAGEMENT ====================

@instructor_required
def instructor_appointments(request):
    """Instructor appointment management page"""
    db = get_db()
    username = request.session.get('admin_username')
    role = request.session.get('admin_role')
    
    # Öğretmenin ad bilgisini bul (ogretmenler koleksiyonundan)
    ogretmen = db.ogretmenler.find_one({'kullanici_adi': username})
    
    if not ogretmen:
        # Eğer ogretmenler koleksiyonunda yoksa, kullanıcı adını direkt kullan
        ogretmen_adi = username
    else:
        ogretmen_adi = ogretmen.get('ad', username)
    
    # Filtreleme
    status_filter = request.GET.get('status', 'bekliyor')
    
    query = {'ogretmen_adi': ogretmen_adi}
    if status_filter and status_filter != 'all':
        query['durum'] = status_filter
    
    appointments_raw = list(db.randevular.find(query).sort('olusturma_tarihi', -1))
    
    # Serialize appointments for template
    appointments = []
    for apt in appointments_raw:
        apt['id'] = str(apt['_id'])
        appointments.append(apt)
    
    # İstatistikler
    total = db.randevular.count_documents({'ogretmen_adi': ogretmen_adi})
    pending = db.randevular.count_documents({'ogretmen_adi': ogretmen_adi, 'durum': 'bekliyor'})
    approved = db.randevular.count_documents({'ogretmen_adi': ogretmen_adi, 'durum': 'onaylandi'})
    rejected = db.randevular.count_documents({'ogretmen_adi': ogretmen_adi, 'durum': 'reddedildi'})
    cancelled = db.randevular.count_documents({'ogretmen_adi': ogretmen_adi, 'durum': 'iptal'})
    
    context = {
        'admin_username': username,
        'admin_role': role,
        'ogretmen_adi': ogretmen_adi,
        'appointments': appointments,
        'status_filter': status_filter,
        'stats': {
            'total': total,
            'pending': pending,
            'approved': approved,
            'rejected': rejected,
            'cancelled': cancelled,
        }
    }
    return render(request, 'admin/instructor_appointments.html', context)

@instructor_required
def instructor_approve_appointment(request, appointment_id):
    """Approve appointment by instructor"""
    if request.method == 'POST':
        db = get_db()
        username = request.session.get('admin_username')
        
        # Öğretmenin kendi randevusu mu kontrol et
        ogretmen = db.ogretmenler.find_one({'kullanici_adi': username})
        ogretmen_adi = ogretmen.get('ad', username) if ogretmen else username
        
        appointment = db.randevular.find_one({'_id': ObjectId(appointment_id)})
        
        if not appointment:
            messages.error(request, 'Randevu bulunamadı!')
            return redirect('instructor_appointments')
        
        if appointment.get('ogretmen_adi') != ogretmen_adi:
            messages.error(request, 'Bu randevuyu onaylama yetkiniz yok!')
            return redirect('instructor_appointments')
        
        result = db.randevular.update_one(
            {'_id': ObjectId(appointment_id)},
            {
                '$set': {
                    'durum': 'onaylandi',
                    'onay_tarihi': datetime.now(),
                    'onaylayan': username
                }
            }
        )
        
        if result.modified_count > 0:
            messages.success(request, 'Randevu başarıyla onaylandı!')
        else:
            messages.error(request, 'Randevu onaylanamadı!')
    
    return redirect('instructor_appointments')

@instructor_required
def instructor_reject_appointment(request, appointment_id):
    """Reject appointment by instructor"""
    if request.method == 'POST':
        db = get_db()
        username = request.session.get('admin_username')
        
        # Öğretmenin kendi randevusu mu kontrol et
        ogretmen = db.ogretmenler.find_one({'kullanici_adi': username})
        ogretmen_adi = ogretmen.get('ad', username) if ogretmen else username
        
        appointment = db.randevular.find_one({'_id': ObjectId(appointment_id)})
        
        if not appointment:
            messages.error(request, 'Randevu bulunamadı!')
            return redirect('instructor_appointments')
        
        if appointment.get('ogretmen_adi') != ogretmen_adi:
            messages.error(request, 'Bu randevuyu reddetme yetkiniz yok!')
            return redirect('instructor_appointments')
        
        result = db.randevular.update_one(
            {'_id': ObjectId(appointment_id)},
            {
                '$set': {
                    'durum': 'reddedildi',
                    'red_tarihi': datetime.now(),
                    'reddeden': username
                }
            }
        )
        
        if result.modified_count > 0:
            messages.success(request, 'Randevu reddedildi!')
        else:
            messages.error(request, 'Randevu reddedilemedi!')
    
    return redirect('instructor_appointments')

@instructor_required
def instructor_appointments_table(request):
    """Instructor appointment table view with sorting"""
    db = get_db()
    username = request.session.get('admin_username')
    role = request.session.get('admin_role')
    
    # Öğretmenin ad bilgisini bul
    ogretmen = db.ogretmenler.find_one({'kullanici_adi': username})
    ogretmen_adi = ogretmen.get('ad', username) if ogretmen else username
    
    # Sıralama parametreleri
    sort_by = request.GET.get('sort', 'tarih')
    order = request.GET.get('order', 'desc')
    status_filter = request.GET.get('status', 'all')
    
    # MongoDB sıralama yönü
    sort_direction = -1 if order == 'desc' else 1
    
    # Sıralama alanı eşleştirme
    sort_field_map = {
        'tarih': 'tarih',
        'ogrenci': 'ogrenci_adi',
        'konu': 'konu',
        'durum': 'durum',
        'olusturma': 'olusturma_tarihi'
    }
    sort_field = sort_field_map.get(sort_by, 'tarih')
    
    # Query oluştur
    query = {'ogretmen_adi': ogretmen_adi}
    if status_filter and status_filter != 'all':
        query['durum'] = status_filter
    
    appointments_raw = list(db.randevular.find(query).sort(sort_field, sort_direction))
    
    # Serialize
    appointments = []
    for apt in appointments_raw:
        apt['id'] = str(apt['_id'])
        appointments.append(apt)
    
    context = {
        'admin_username': username,
        'admin_role': role,
        'ogretmen_adi': ogretmen_adi,
        'appointments': appointments,
        'sort_by': sort_by,
        'order': order,
        'status_filter': status_filter,
    }
    return render(request, 'admin/instructor_appointments_table.html', context)

@instructor_required
def instructor_profile(request):
    """Instructor profile page"""
    db = get_db()
    username = request.session.get('admin_username')
    role = request.session.get('admin_role')
    
    # Get user info from Kullanici model
    from Kullanıcılar.models import Kullanici
    try:
        kullanici = Kullanici.objects.get(kullanici_adi=username)
    except Kullanici.DoesNotExist:
        kullanici = None
    
    # Get instructor info from MongoDB
    ogretmen = db.ogretmenler.find_one({'kullanici_adi': username})
    if not ogretmen:
        # Try to find by email
        ogretmen = db.ogretmenler.find_one({'email': username})
    
    if request.method == 'POST' and ogretmen:
        # Update allowed fields
        updates = {}
        bolum = request.POST.get('bolum')
        ofis = request.POST.get('ofis')
        telefon = request.POST.get('telefon')
        
        if bolum: updates['bolum'] = bolum
        if ofis: updates['ofis'] = ofis
        if telefon: updates['telefon'] = telefon
        
        if updates:
            db.ogretmenler.update_one(
                {'_id': ogretmen['_id']},
                {'$set': updates}
            )
            messages.success(request, 'Profil bilgileriniz başarıyla güncellendi.')
            # Refresh data
            ogretmen = db.ogretmenler.find_one({'_id': ogretmen['_id']})
    
    # Get appointment stats
    ogretmen_adi = ogretmen.get('ad', username) if ogretmen else username
    stats = {
        'total': db.randevular.count_documents({'ogretmen_adi': ogretmen_adi}),
        'pending': db.randevular.count_documents({'ogretmen_adi': ogretmen_adi, 'durum': 'bekliyor'}),
        'approved': db.randevular.count_documents({'ogretmen_adi': ogretmen_adi, 'durum': 'onaylandi'}),
        'rejected': db.randevular.count_documents({'ogretmen_adi': ogretmen_adi, 'durum': 'reddedildi'}),
    }
    
    context = {
        'admin_username': username,
        'admin_role': role,
        'kullanici': kullanici,
        'ogretmen': ogretmen,
        'ogretmen_adi': ogretmen_adi,
        'ogretmen_unvan': ogretmen.get('unvan', '—') if ogretmen else '—',
        'stats': stats,
    }
    return render(request, 'admin/instructor_profile.html', context)


@instructor_required
def instructor_change_password(request):
    """Instructor password change page"""
    username = request.session.get('admin_username')
    role = request.session.get('admin_role')
    
    # Get instructor info from MongoDB
    db = get_db()
    ogretmen = db.ogretmenler.find_one({'kullanici_adi': username})
    if not ogretmen:
        ogretmen = db.ogretmenler.find_one({'email': username})
    
    ogretmen_adi = ogretmen.get('ad', username) if ogretmen else username
    
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validate
        from Kullanıcılar.models import Kullanici
        try:
            kullanici = Kullanici.objects.get(kullanici_adi=username)
            
            if not kullanici.check_password(current_password):
                messages.error(request, 'Mevcut şifreniz hatalı!')
            elif new_password != confirm_password:
                messages.error(request, 'Yeni şifreler eşleşmiyor!')
            elif len(new_password) < 6:
                messages.error(request, 'Yeni şifre en az 6 karakter olmalıdır!')
            else:
                kullanici.set_password(new_password)
                kullanici.save()
                messages.success(request, 'Şifreniz başarıyla değiştirildi!')
                return redirect('instructor_profile')
        except Kullanici.DoesNotExist:
            messages.error(request, 'Kullanıcı bulunamadı!')
    
    context = {
        'admin_username': username,
        'admin_role': role,
        'ogretmen_adi': ogretmen_adi,
    }
    return render(request, 'admin/instructor_change_password.html', context)


# ==================== CLUB MANAGEMENT ====================

@admin_required
def admin_clubs(request):
    """Club management"""
    db = get_db()
    
    # Filtreleme
    kategori = request.GET.get('kategori')
    status = request.GET.get('status', 'all')
    
    query = {}
    if kategori:
        query['kategori'] = kategori
    
    if status and status != 'all':
        query['durum'] = status
    
    clubs_raw = list(db.kulupler.find(query).sort('olusturma_tarihi', -1))
    
    clubs = []
    for club in clubs_raw:
        club['id'] = str(club['_id'])
        clubs.append(club)
    
    context = {
        'admin_username': request.session.get('admin_username'),
        'admin_role': request.session.get('admin_role'),
        'clubs': clubs,
        'selected_kategori': kategori,
        'selected_status': status,
    }
    return render(request, 'admin/clubs.html', context)

@admin_required
def approve_club(request, club_id):
    """Approve club suggestion"""
    if request.method == 'POST':
        db = get_db()
        result = db.kulupler.update_one(
            {'_id': ObjectId(club_id)},
            {
                '$set': {
                    'durum': 'onaylandi',
                    'onay_tarihi': datetime.now(),
                    'onaylayan': request.session.get('admin_username')
                }
            }
        )
        if result.modified_count > 0:
            messages.success(request, 'Kulüp onaylandı!')
        else:
            messages.error(request, 'İşlem başarısız oldu.')
    return redirect('admin_clubs')

@admin_required
def reject_club(request, club_id):
    """Reject club suggestion"""
    if request.method == 'POST':
        db = get_db()
        result = db.kulupler.update_one(
            {'_id': ObjectId(club_id)},
            {
                '$set': {
                    'durum': 'reddedildi',
                    'red_tarihi': datetime.now(),
                    'reddeden': request.session.get('admin_username')
                }
            }
        )
        if result.modified_count > 0:
            messages.success(request, 'Kulüp reddedildi!')
        else:
            messages.error(request, 'İşlem başarısız oldu.')
    return redirect('admin_clubs')

@admin_required
def delete_club(request, club_id):
    """Delete club"""
    if request.method == 'POST':
        db = get_db()
        result = db.kulupler.delete_one({'_id': ObjectId(club_id)})
        if result.deleted_count > 0:
            messages.success(request, 'Kulüp silindi!')
        else:
            messages.error(request, 'Silme işlemi başarısız.')
    return redirect('admin_clubs')


@admin_required
def assign_club_president(request):
    """Assign a president to a club"""
    db = get_db()
    
    # Get all approved clubs (sort by name)
    clubs_raw = list(db.kulupler.find({'durum': 'onaylandi'}).sort('ad', 1))
    
    clubs_without_president = []
    clubs_with_president = []
    
    for c in clubs_raw:
        c['id'] = str(c['_id'])
        # Check if club has a president assigned
        if c.get('baskan_id') or c.get('baskan_username'):
            clubs_with_president.append(c)
        else:
            clubs_without_president.append(c)
    
    if request.method == 'POST':
        club_id = request.POST.get('club_id')
        username = request.POST.get('username')  # This is the school number
        president_name = request.POST.get('president_name', '').strip()
        president_email = request.POST.get('president_email', '').strip()
        
        try:
            from Kullanıcılar.models import Kullanici
            
            # Check club exists
            if not club_id:
                messages.error(request, 'Lütfen bir kulüp seçin.')
                return redirect('assign_club_president')
            
            # First, try to find user by school number (username)
            user = None
            validation_errors = []
            
            # Search by school number (okul_numarasi)
            try:
                user = Kullanici.objects.get(okul_numarasi=username)
            except Kullanici.DoesNotExist:
                # Try by username as fallback
                try:
                    user = Kullanici.objects.get(kullanici_adi=username)
                except Kullanici.DoesNotExist:
                    validation_errors.append(f'Okul numarası veya kullanıcı adı "{username}" ile kayıtlı kullanıcı bulunamadı.')
            
            if user:
                # Validate name matches
                if president_name and user.isim:
                    if president_name.lower() != user.isim.lower():
                        validation_errors.append(f'Girilen isim ({president_name}) sistemdeki isimle ({user.isim}) eşleşmiyor.')
                
                # Validate email matches
                if president_email and user.email:
                    if president_email.lower() != user.email.lower():
                        validation_errors.append(f'Girilen e-posta ({president_email}) sistemdeki e-posta ({user.email}) ile eşleşmiyor.')
            
            # If there are validation errors, show them
            if validation_errors:
                for error in validation_errors:
                    messages.error(request, error)
                return redirect('assign_club_president')
            
            if not user:
                messages.error(request, 'Kullanıcı bulunamadı!')
                return redirect('assign_club_president')
                
            # Update User Role
            user.rol = 'club_moderator'
            user.save()
            
            # Update Club Document with detailed info
            db.kulupler.update_one(
                {'_id': ObjectId(club_id)},
                {
                    '$set': {
                        'baskan_id': user.id,
                        'baskan_username': user.kullanici_adi,
                        'baskan_isim': user.isim or president_name or user.kullanici_adi,
                        'baskan_email': user.email or president_email,
                        'baskan_okul_numarasi': user.okul_numarasi or username
                    }
                }
            )
            
            messages.success(request, f'{user.isim or user.kullanici_adi} başarıyla kulüp başkanı olarak atandı! ✓ Bilgiler doğrulandı.')
            return redirect('assign_club_president')
            
        except Exception as e:
            messages.error(request, f'Hata oluştu: {str(e)}')
            
    context = {
        'admin_username': request.session.get('admin_username'),
        'admin_role': request.session.get('admin_role'),
        'clubs_without_president': clubs_without_president,
        'clubs_with_president': clubs_with_president,
    }
    return render(request, 'admin/assign_president.html', context)


@superadmin_required
def remove_club_president(request):
    """Remove president from a club"""
    from django.http import JsonResponse
    from Kullanıcılar.models import Kullanici
    from Core.mongodb_utils import get_db
    
    db = get_db()
    
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'POST required'})
    
    club_id = request.POST.get('club_id')
    
    if not club_id:
        return JsonResponse({'success': False, 'error': 'Kulüp ID gerekli'})
    
    try:
        # Get club info first to find current president
        club = db.kulupler.find_one({'_id': ObjectId(club_id)})
        
        if not club:
            return JsonResponse({'success': False, 'error': 'Kulüp bulunamadı'})
        
        # Get current president's user id
        baskan_id = club.get('baskan_id')
        baskan_username = club.get('baskan_username')
        
        # Reset user role to 'user' if found
        if baskan_id:
            try:
                user = Kullanici.objects.get(id=baskan_id)
                user.rol = 'user'
                user.save()
            except Kullanici.DoesNotExist:
                pass
        elif baskan_username:
            try:
                user = Kullanici.objects.get(kullanici_adi=baskan_username)
                user.rol = 'user'
                user.save()
            except Kullanici.DoesNotExist:
                pass
        
        # Remove president info from club
        db.kulupler.update_one(
            {'_id': ObjectId(club_id)},
            {
                '$unset': {
                    'baskan_id': '',
                    'baskan_username': '',
                    'baskan_isim': '',
                    'baskan_email': '',
                    'baskan_okul_numarasi': ''
                }
            }
        )
        
        return JsonResponse({'success': True})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

