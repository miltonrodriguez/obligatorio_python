from django.db import models
import datetime
from django.utils import timezone
from _overlapped import NULL
from tkinter.constants import CURRENT
# Create your models here.

class Libro(models.Model):
    isbn = models.PositiveIntegerField(primary_key=True)
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    fecha_ingreso = models.DateField()
    
    def __str__(self):
        return "ISBN {} titulo {}".format(self.isbn,self.titulo)

class Ejemplar(models.Model):
    num_inventario = models.AutoField(primary_key=True)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    disponible = models.BooleanField(default = True)
    
    def __str__(self):
        return "Nro {} Disponible {} Libro {}".format(self.num_inventario,self.disponible, self.libro)

class Socio(models.Model):
    documento = models.PositiveIntegerField(primary_key=True)
    nombre = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    fecha_nacimiento = models.DateField()
    moroso = models.BooleanField(default = False)
    
    def __str__(self):
        return "Doc {} Nombre {}".format(self.documento,self.nombre)
    
class Prestamo(models.Model):
    ejemplar = models.ForeignKey(Ejemplar, on_delete=models.CASCADE)
    socio = models.ForeignKey(Socio, on_delete=models.CASCADE)
    fecha_ini = models.DateField()
    fecha_fin = models.DateField(null=True,default=NULL)
    devuelto = models.BooleanField(default = False)

    def __str__(self):
        return "Ejemplar {} Fecha Ini {} Devuelto {} Socio {}".format(self.ejemplar,self.fecha_ini,self.devuelto,self.socio)


