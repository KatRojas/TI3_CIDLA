from django.db import models
from djongo import models

# Create your models here.
class Data(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)

#estructura de prueba para ingresar datos a la db y luego poder graficarlos
class Posts(models.Model):
    #para asignar el tipo de dato, se tiene que ver Django model data types (formato que usa django)
    _id=models.ObjectIdField() #retorna un objeto  
    post_title=models.CharField(max_length=255)
    post_description=models.TextField()
    comment=models.JSONField() #se le asigna formato JSON para ingresar datos
    tags=models.JSONField()
    user_details=models.JSONField()
    objects=models.DjongoManager()