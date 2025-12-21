from django.shortcuts import render, redirect
from Kullanıcılar.decorators import kullanici_login_required
from django.contrib import messages
from Core.mongodb_utils import get_db
from datetime import datetime

@kullanici_login_required
def kulupOner(request):
    if request.method == 'POST':
        ad = request.POST.get('ad')
        kategori = request.POST.get('kategori')
        aciklama = request.POST.get('aciklama')
        # Additional fields
        uyesayisi = request.POST.get('uyesayisi')
        faaliyetler = request.POST.get('faaliyetler')
        katki = request.POST.get('katki')
        iletisim_isim = request.POST.get('iletisim_isim')
        okul_mail = request.POST.get('okul_mail')
        
        try:
            db = get_db()
            db.kulupler.insert_one({
                'ad': ad,
                'kategori': kategori,
                'aciklama': aciklama,
                'uyesayisi': uyesayisi,
                'faaliyetler': faaliyetler,
                'katki': katki,
                'iletisim_isim': iletisim_isim,
                'okul_mail': okul_mail,
                'kurucu_id': request.session.get('user_id'),
                'kurucu_username': request.session.get('user_username'),
                'uye_ids': [],
                'durum': 'bekliyor', # Onay mekanizması için eklendi
                'olusturma_tarihi': datetime.now()
            })
            # messages.success(request, 'Kulüp öneriniz başarıyla gönderildi!')
            return render(request, "kulupOner.html", {'success': True})
        except Exception as e:
            messages.error(request, f'Kulüp oluşturulurken bir hata oluştu: {str(e)}')
    
    return render(request, "kulupOner.html")
