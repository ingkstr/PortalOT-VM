"""Modelos de ordenes"""
from django.db import models
from catalogos.models import *
from datetime import datetime

class Orden(models.Model):
    """Clase modelo de orden de trabajo o ventana de mantenimiento"""
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
    fecha_inicio_afectacion = models.DateField(blank = True, null = True)
    hora_inicio_afectacion = models.TimeField(blank = True, null = True)
    fecha_fin_afectacion = models.DateField(blank = True, null = True)
    hora_fin_afectacion = models.TimeField(blank = True, null = True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    ejecutores = models.ManyToManyField(Ejecutor)
    mop = models.FileField(upload_to='mops')
    servicios = models.ManyToManyField(Servicio, blank = True)
    clientes_afectados = models.CharField(max_length=500, blank = True, null = True)
    comentarios = models.CharField(max_length=250, blank = True, null = True)
    estatus = models.IntegerField(default = 0)
    log = models.TextField(default = "Orden creada en "+ str(datetime.now()))
