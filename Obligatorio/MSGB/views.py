from django.shortcuts import render
from .models import Socio, Prestamo, Libro

# Create your views here.




def libros_prestados(doc_socio):
        fecha = datetime.date.today()
        for prestamo in Socio