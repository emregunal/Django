"""
Admin Panel Views
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from Core.admin_auth import admin_required, authenticate_admin
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
        
        if authenticate_admin(username, password):
            request.session['is_admin'] = True
            request.session['admin_username'] = username
            messages.success(request, f'Hoş geldiniz, {username}!')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Kullanıcı adı veya şifre hatalı!')
    
    return render(request, 'admin/login.html')

@admin_required
def admin_dashboard(request):
    """Admin dashboard"""
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

@admin_required
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
    request.session.flush()
    messages.success(request, 'Başarıyla çıkış yaptınız.')
    return redirect('admin_login')
