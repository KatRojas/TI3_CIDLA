from django.http import HttpResponse
from pymongo import MongoClient
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
import datetime
import pandas as pd
import csv
import json
import pymongo


# Request: Para realizar peticiones al servidor
# HttpResponse: Sirve para enviar la respuesta usando el protocolo HTTP.

#Estas son vistas de prueba
def inicio(request):  #Pasamos un objeto de tipo request como primer argumento
    ramo = "Taller integracion 3" #variable con texto
    fecha = datetime.datetime.now() #sacamos fecha
    return render(request,'inicio.html',{"Ramo": ramo, "fecha": fecha} )#parametros 1- request, 2- nombre plantilla, 3- contexto (variables)


def archivos(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['uploadedfile']
        if uploaded_file:
            ext = uploaded_file.name.split('.')[-1]
            if ext != 'csv' and ext != 'json' and ext != 'xlsx':
                messages.add_message(request, messages.INFO, 'El archivo seleccionado no tiene uno de los formatos solicitados  CSV, JSON o XLSX')
            elif ext == 'csv':
                messages.add_message(request, messages.INFO, 'El archivo seleccionado se guardo correctamente.')
                fs = FileSystemStorage()
                fs.save(uploaded_file.name, uploaded_file)
                mongodb = MongoDB(dBName = 'ti3', collectionName='archivocsv')
                mongodb.InsertData(path='media/'+uploaded_file.name)
            elif ext == 'json':
                #messages.add_message(request, messages.INFO, 'El archivo seleccionado es tipo json')
                messages.add_message(request, messages.INFO, 'El archivo seleccionado se guardo correctamente.')
                fs = FileSystemStorage()
                fs.save(uploaded_file.name, uploaded_file)
                mongodb = MongoDB(dBName = 'ti3', collectionName='archivojson')
                mongodb.InsertData2(path='media/'+uploaded_file.name)
                #inserta archivos json cuando son puros, no cuando tienen al inicio un $oid...
                #EJ: "$oid": "5f53adf7bfabf87f57ea6020"
            else:
                if ext == 'xlsx':
                    # messages.add_message(request, messages.INFO, 'El archivo seleccionado es tipo xlsx')
                    messages.add_message(request, messages.INFO, 'El archivo seleccionado se guardo correctamente.')
                    fs = FileSystemStorage()
                    fs.save(uploaded_file.name, uploaded_file)
                    mongodb = MongoDB(dBName = 'ti3', collectionName='archivoexcel')
                    mongodb.InsertData3(path='media/'+uploaded_file.name)



    return render(request,'archivos.html')#parametros 1- request, 2- nombre plantilla, 3- contexto (variables)

class MongoDB(object):

    def __init__(self, dBName=None, collectionName=None):

        self.dBName = dBName
        self.collectionName = collectionName

        self.client = MongoClient("localhost", 27017, maxPoolSize=50)

        self.DB = self.client[self.dBName]
        self.collection = self.DB[self.collectionName]



    def InsertData(self, path=None):
        """
        :param path: Path os csv File
        :return: None
        """

        df = pd.read_csv(path)
        data = df.to_dict('records')

        self.collection.insert_many(data, ordered=False)
        print("All the Data has been Exported to Mongo DB Server .... ")

    def InsertData2(self, path=None):

        with open(path) as file: 
            file_data = json.load(file) 

        if isinstance(file_data, list): 
            self.collection.insert_many(file_data)   
        else: 
            self.collection.insert_one(file_data)

    def InsertData3(self, path=None):

        df = pd.read_excel(path)
        data = df.to_dict('records')

        self.collection.insert_many(data, ordered=False)
        print("All the Data has been Exported to Mongo DB Server .... ")       
    