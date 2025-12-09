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
        
        try:
            db = get_db()
            db.kulupler.insert_one({
                'ad': ad,
                'kategori': kategori,
                'aciklama': aciklama,
                'kurucu_id': request.session.get('user_id'),
                'kurucu_username': request.session.get('user_username'),
                'uye_ids': [],
                'olusturma_tarihi': datetime.now()
            })
            messages.success(request, 'Kulüp öneriniz başarıyla gönderildi!')
            return redirect('kulupler')
        except Exception as e:
            messages.error(request, f'Kulüp oluşturulurken bir hata oluştu: {str(e)}')
    
    return render(request, "kulupOner.html")
