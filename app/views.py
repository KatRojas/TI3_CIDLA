from django.shortcuts import render
from django.http import HttpResponse
from .models import Data

# Create your views here.
def info(request):
    inf = Data.objects.all()
    a = []
    for field in inf:
        a.append([field.nombre,field.apellido])
    return render(request,'info.html',{"Data": a})