"""Modelos de ordenes"""
from django.db import models
from catalogos.models import *

class Orden(models.Model):
    id = models.CharField(primary_key=True, max_length=10, unique=True)
    actividad = models.CharField(max_length=2)
    gerencia = models.ForeignKey(Gerencia, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE)
    contacto = models.CharField(max_length=10)
    asunto = models.CharField(max_length=50)
    detalle = models.CharField(max_length=250)
    localidades = models.ManyToManyField(Localidad)
    fecha_inicio = models.DateField()
    hora_inicio = models.TimeField()
    fecha_fin = models.DateField()
    hora_fin = models.TimeField()
