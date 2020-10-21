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

# Create your views here.
def info(request):
    #inf = Data.objects.all()
    #a = []
    #for field in inf:
    #    a.append([field.nombre,field.apellido])
    total = 0
    cc1 = 0
    cc2 = 0
    posts=Posts.objects.all() #en la variable posts guardamos todos los datos que saquemos de la estructura
    stringval=""
    for post in posts: #creamos un ciclo para recorrer los datos
        stringval += "First Name : " + post.user_details['first_name'] + " Last name : " + post.user_details[
            'last_name'] + " Post Title " + post.post_title + " Comment " + post.comment[0]+"<br>"
        total+=1
        nombre = post.user_details['first_name'].lower() #extraemos el nombre y aplicamos lower para colocar el texto en minuscula
        if nombre == "bryan":
            cc1= cc1+1
        elif nombre  == "diego":
            cc2=cc2+1
    names = ['Bryan','Diego']
    values = [cc1,cc2]

    plt.figure(figsize=(9, 3)) #creamos la figura
    plt.suptitle('Graficos')
    #subplot nos permite crear distintos graficos para mostrar, subplot(Un entero de 3 dígitos o tres enteros independientes que describen la posición del subgráfico)
    plt.subplot(131)
    plt.bar(names, values)
    plt.subplot(132)
    plt.scatter(names, values)
    plt.subplot(133)
    plt.title('Graficos de Torta')
    explode = [0,0]  # Destacar algunos
    plt.pie(values, labels=names, explode=explode,
        autopct='%1.1f%%')
    # autopct: El porcentaje correspondiente a cada ítem se puede indicar mediante el argumento 
    #
    
    fig = plt.gcf() #obtenemos la figura actual
    #convert graph into dtring buffer and then we convert 64 bit code into image
    buf = io.BytesIO() #estructura binaria
    fig.savefig(buf,format='png') #guardamos la figura con el formato y estructura
    buf.seek(0)
    #establece la posición actual del archivo en el desplazamiento. El argumento whence es opcional y el valor predeterminado es 0, lo que significa posicionamiento absoluto del archivo
    #otros valores son 1 lo que significa buscar en relación con la posición actual y 2 significa buscar en relación con el final del archivo.
    string = base64.b64encode(buf.read()) #Codificamos el objeto de tipo bytes mediante Base64 y se devuelven los bytes codificados.
    uri =  urllib.parse.quote(string) 
    #parse.quote nos permite citar localmente y hacer versiones seguras de las cadenas que contienen
    #caracteres especiales dentro de los argumentos de consulta que podrían causar problemas en el análisis de la URL en el lado del servidor
    return render(request,'info.html',{"stringval": stringval, "cc1": cc1,"cc2":cc2,"data":uri,"total": total}) 
    #parametros  del render (1- request, 2- nombre plantilla, 3- contexto (variables))


@csrf_exempt
def add_post(request):
    comment=request.POST.get("comment").split(",")
    tags=request.POST.get("tags").split(",")
    user_details={"first_name":request.POST.get("first_name"),"last_name":request.POST.get("last_name")}
    post=Posts(post_title=request.POST.get("post_title"),post_description=request.POST.get("post_description"),comment=comment,tags=tags,user_details=user_details)
    post.save()
    return HttpResponse("Inserted")