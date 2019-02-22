from django.db import models

class Gerencia(models.Model):
    """Clase modelo de una Gerencia de la empresa"""
    nombre = models.CharField(max_length=25, unique=True)
    activo = models.BooleanField()

    def __str__(self):
       return 'Gerencia: ' + self.nombre

class Supervisor(models.Model):
    """Clase modelo de un Supervisor de una Gerencia"""
    nombre = models.CharField(max_length=50, unique=True)
    telefono = models.CharField(max_length=10)
    gerencia= models.ForeignKey(Gerencia, on_delete=models.CASCADE)
    activo = models.BooleanField()

    def __str__(self):
       return 'Supervisor: ' + self.nombre

class Localidad(models.Model):
    """Clase modelo de una Localidad de la empresa"""
    clli = models.CharField(primary_key=True, max_length=10, unique=True)
    localidad = models.CharField(max_length=25)
    ubicacion = models.CharField(max_length=75)
    codigo = models.CharField(max_length=4)
    activo = models.BooleanField()

    def __str__(self):
       return 'Localidad: ' + self.clli + ' '+ self.localidad

class Proveedor(models.Model):
    """Clase modelo de un Proveedor de la empresa"""
    nombre = models.CharField(max_length=50, unique=True)
    codigo = models.CharField(max_length=4)
    activo = models.BooleanField()

    def __str__(self):
       return 'Proveedor: ' + self.nombre

class Ejecutor(models.Model):
    """Clase modelo de un Ejecutor de un proveedor"""
    nombre = models.CharField(max_length=50, unique=True)
    proveedor= models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    activo = models.BooleanField()

    def __str__(self):
       return 'Ejecutor: ' + self.nombre

class Servicio(models.Model):
    """Clase modelo de un servicio ofrecido de la empresa"""
    nombre = models.CharField(max_length=50, unique=True)
    activo = models.BooleanField()

    def __str__(self):
       return 'Servicio: ' + self.nombre
