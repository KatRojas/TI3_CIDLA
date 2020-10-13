from django.http import HttpResponse
import datetime
from django.shortcuts import render

# Request: Para realizar peticiones al servidor
# HttpResponse: Sirve para enviar la respuesta usando el protocolo HTTP.

#Estas son vistas de prueba
def inicio(request):  #Pasamos un objeto de tipo request como primer argumento
    ramo = "Taller integracion 3" #variable con texto
    fecha = datetime.datetime.now() #sacamos fecha
    return render(request,'inicio.html',{"Ramo": ramo, "fecha": fecha} )#parametros 1- request, 2- nombre plantilla, 3- contexto (variables)

