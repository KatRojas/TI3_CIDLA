from django.http import HttpResponse
from pymongo import MongoClient
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.contrib import messages #messages para los mensajes 
from bson.json_util import loads #loads para analizar archivo json
import datetime
import pandas as pd #importamos panda para el manejo de archivos
import csv 
import json
import pymongo


# Request: Para realizar peticiones al servidor
# HttpResponse: Sirve para enviar la respuesta usando el protocolo HTTP.

#Estas son vistas de prueba
def inicio(request):  #Pasamos un objeto de tipo request como primer argumento
    client = MongoClient('localhost',27017)
    db = client.ti3
    col = db.archivojson
    SiNo = True

    if request.method == 'POST': #verificamos si recibimos algo por post
        if request.POST.get('sesiones'): #vemos si viene con informacion
            search = request.POST['search']
            cursor = col.find({"rut":search})
            return render(request,'sesiones.html',{"cursor":cursor}) 

        elif request.POST.get('graficos'):
            search = request.POST['search']
            cursor = col.find({"rut":search})
            return render(request,'graficos.html',{"cursor":cursor})

    else:
        cursor = col.find({})
        return render(request,'inicio.html',{"cursor":cursor}) 

def archivos(request): 
    if request.method == 'POST':  #indicamos que recibiremos algo por metodo POST
        uploaded_file = request.FILES['uploadedfile'] #recibimos el dato que viene con el nombre del archivo
        if uploaded_file:
            ext = uploaded_file.name.split('.')[-1] #separamos el nombre para pode dejar solo la extencion
            if ext != 'csv' and ext != 'json' and ext != 'xlsx': #si el archivo no tiene ni uno de esos 3 formatos mandara un mensaje de error
                messages.add_message(request, messages.INFO, 'El archivo seleccionado no tiene uno de los formatos solicitados  CSV, JSON o XLSX')
            elif ext == 'csv': #si el archivo tiene formato csv
                messages.add_message(request, messages.INFO, 'El archivo seleccionado se guardo correctamente.')
                fs = FileSystemStorage() #almacenamiento de archivos en un sistema de archivos local
                fs.save(uploaded_file.name, uploaded_file) #guardamos el archivo indicando el nombre
                mongodb = MongoDB(dBName = 'ti3', collectionName='archivocsv') #indicamos la db y la coleccion donde queremos guardar los datos
                mongodb.InsertData(path='media/'+uploaded_file.name) #indicamos la ruta del archivo para guardar

            elif ext == 'json': #si el archivo tiene formato json
                #messages.add_message(request, messages.INFO, 'El archivo seleccionado es tipo json')
                messages.add_message(request, messages.INFO, 'El archivo seleccionado se guardo correctamente.')
                fs = FileSystemStorage()#almacenamiento de archivos en un sistema de archivos local
                fs.save(uploaded_file.name, uploaded_file)#almacenamiento de archivos en un sistema de archivos local
                mongodb = MongoDB(dBName = 'ti3', collectionName='archivojson')#guardamos los datos indicando la db y la colleccion
                mongodb.InsertData2(path='media/'+uploaded_file.name) #indicamos la ruta del archivo para guardar

            else:
                if ext == 'xlsx': #si el archivo tiene formato xlsx
                    # messages.add_message(request, messages.INFO, 'El archivo seleccionado es tipo xlsx')
                    messages.add_message(request, messages.INFO, 'El archivo seleccionado se guardo correctamente.')
                    fs = FileSystemStorage()#almacenamiento de archivos en un sistema de archivos local
                    fs.save(uploaded_file.name, uploaded_file)#almacenamiento de archivos en un sistema de archivos local
                    mongodb = MongoDB(dBName = 'ti3', collectionName='archivoexcel')#guardamos los datos indicando la db y la colleccion
                    mongodb.InsertData3(path='media/'+uploaded_file.name) #indicamos la ruta del archivo para guardar



    return render(request,'archivos.html')#parametros 1- request, 2- nombre plantilla, 3- contexto (variables)

class MongoDB(object): #creamos una clase para crear la conexion directa y guardar los rachivos en la db

    def __init__(self, dBName=None, collectionName=None):

        self.dBName = dBName
        self.collectionName = collectionName

        self.client = MongoClient("localhost", 27017, maxPoolSize=50)

        self.DB = self.client[self.dBName]
        self.collection = self.DB[self.collectionName]



    def InsertData(self, path=None): #funcion para insertar datos csv
        """
        :param path: Path os csv File
        :return: None
        """

        df = pd.read_csv(path) #leemos archivo indicando el formato csv 
        data = df.to_dict('records') #convertimos a diccionario

        self.collection.insert_many(data, ordered=False) #guardamos los datos
        print("All the Data has been Exported to Mongo DB Server .... ")

    def InsertData2(self, path=None): #funcion para insertar datos json

        with open(path,'r',errors='ignore') as file: 
            s = file.read() #leemos los datos del archivo json
            if "$oid" in s:
                #s = s.replace('\'','\"')
                s = s.replace("': '", '": "').replace("', '", '", "').replace("{'", '{"').replace("'}", '"}').replace("': \"", '": "').replace("', \"", '", "').replace("\", '", '", "').replace("'", '\\"')
                #reenplazamos los caracteres para ingresar correctamente los datos del json sin problemas
            data = loads(s) #analizamos el archivo json con el metodo load (el resultado es un diccionario en python)

        #insertamos el dato en la db
        if isinstance(data, list): 
            self.collection.insert_many(data)   
        else: 
            self.collection.insert_one(data)

    def InsertData3(self, path=None):#funcion para insertar datos excel

        df = pd.read_excel(path) #leemos el archivo indicando que es excel
        data = df.to_dict('records') #convertimos a diccionario

        self.collection.insert_many(data, ordered=False) #insertamos los datos en la db
        print("All the Data has been Exported to Mongo DB Server .... ")       
    