from bson import ObjectId #importamos bson para el intercambio de datos con mongo
from django.http import HttpResponse #es el mensaje que envía el servidor al cliente tras haber recibido una petición o HTTP request
from django.shortcuts import render #atajo para mostrar las plantillas

# Create your views here.
from app.models import Posts #importamos el modelo "Posts" de models para tener la estructura de los datos
from django.views.decorators.csrf import csrf_exempt #importamos csrf_exempt para proveer protección contra Cross-site request forgery (falsificación de peticiones inter-sitio)
import matplotlib.pyplot as plt #importamos matplotlib para los graficos
import io 
#io El módulo io implementa las clases detrás de la función open() 
# incorporada del intérprete para operaciones de entrada y salida basadas en archivos. Las clases se descomponen de tal manera que pueden ser recombinadas
import urllib, base64
#urllib proporciona una interfaz de programación para usar recursos de Internet identificados por URLs
#base64 contiene funciones para traducir datos binarios en un subconjunto de ASCII adecuado para la transmisión utilizando protocolos de texto plano

from .models import Data
from pymongo import MongoClient
from datetime import datetime

# Create your views here.
def info(request):
    data = ''
    dd = ''
    dato_sesiones = []
    data_personal = []
    SiNo = True
    msj = "Complete todos lo datos Solicitados"
    
    if request.method == 'POST':

        search = request.POST['search']
        inicio = request.POST['inicio']
        fin = request.POST['fin']
        
        if search == '' or inicio == '' or fin == '':
            SiNo = False
        else:
            inicio1 = inicio.split("-")
            inicio2 = inicio1[0]+"-"+inicio1[1]+"-"+inicio1[2]
            fin1 = fin.split("-")
            fin2 = fin1[0]+"-"+fin1[1]+"-"+fin1[2]

            inicio3 = datetime.strptime(inicio2,'%Y-%m-%d')
            fin3 = datetime.strptime(fin2,'%Y-%m-%d')

            client = MongoClient('localhost',27017)
            db = client.ti3
            col = db.archivojson
            cursor = col.find({ 'rut':search })
            for x in cursor:
                data = x['nombre'] + ' ' + x['apellidos']
                data_personal.append(x['nombre'])
                data_personal.append(x['apellidos'])
                data_personal.append(x['rut'])
                data_personal.append(x['direccion'])
                data_personal.append(x['fecha_nacimiento'])
                data_personal.append(x['ciudad'])
                for y in range(len(x['sesiones_medica'])):
                    fec = x['sesiones_medica'][y]['fecha']
                    if datetime.strptime(fec,'%Y-%m-%d') >= inicio3 and datetime.strptime(fec,'%Y-%m-%d') <= fin3:
                        dato_sesiones.append([x["sesiones_medica"][y]])
                        ff = x['sesiones_medica'][y]['fecha']
                        if dd == '':
                            dd = ff
                        else:
                            dd = dd +','+ ff
    if SiNo == False:
        return render(request,'info.html',{"msj":msj})
    else:
        return render(request,'info.html',{"data":data,"dato_fecha":dd,"sesiones":dato_sesiones,"personal":data_personal}) 


@csrf_exempt
def add_post(request):
    comment=request.POST.get("comment").split(",")
    tags=request.POST.get("tags").split(",")
    user_details={"first_name":request.POST.get("first_name"),"last_name":request.POST.get("last_name")}
    post=Posts(post_title=request.POST.get("post_title"),post_description=request.POST.get("post_description"),comment=comment,tags=tags,user_details=user_details)
    post.save()
    return HttpResponse("Inserted")
