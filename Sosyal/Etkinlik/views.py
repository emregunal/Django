from django.shortcuts import render
from django.http.response import HttpResponse
from Kullanıcılar.decorators import kullanici_login_required


@kullanici_login_required
def etkinlik(request, id):
  return render(request, "etkinlik.html")