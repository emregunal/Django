from django.shortcuts import render
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required(login_url='/Kullanıcılar/login/')
def etkinlik(request, id):
  return render(request, "etkinlik.html")