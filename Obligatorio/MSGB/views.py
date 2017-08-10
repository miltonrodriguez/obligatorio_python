from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from datetime import  date, timedelta
from .models import Socio, Prestamo, Libro, Ejemplar
from .forms import SocioForm
from builtins import int
from django.template import loader
from django.template.context_processors import request
from _overlapped import NULL


# Create your views here.

def index(request):
    template = loader.get_template('MSGB/index.html')
    return HttpResponse(template.render())

def prestamo(request):
    return redirect("index")

def devolucion(request):
    return redirect("index")

def info_socio(request, documento):
    id = int(documento)
    socio = get_object_or_404(Socio, pk=id)
    prestamo_list = socio.prestamo_set.all()
    template = loader.get_template('MSGB/info_socio.html')
    context = {
        'socio': socio,
        'prestamo_list': prestamo_list,
    }
    return HttpResponse(template.render(context, request))

def list_socios(request):
    socios_list = Socio.objects.all().order_by('documento')
    template = loader.get_template('MSGB/listado_socios.html')
    context = {        
        'socios_list': socios_list,
    }
    return HttpResponse(template.render(context, request))

def info_libro(request, isbn):
    id = int(isbn)
    libro = get_object_or_404(Libro, pk=id)
    copias_list = libro.ejemplar_set.all()
    template = loader.get_template('MSGB/info_libro.html')
    context = {
        'libro': libro,
        'copias_list': copias_list,
    }
    return HttpResponse(template.render(context, request))

def info_copia(request, num_inventario):
    id = int(num_inventario)
    copia = get_object_or_404(Ejemplar, pk=id)
    #si la copia esta prestada busco al socio que lo tiene
    socio, prestamo = NULL, NULL
    if not copia.disponible:
        prestamo = Prestamo.objects.filter(devuelto = False, ejemplar_id=id).first()
        socio = prestamo.socio          
    template = loader.get_template('MSGB/info_copia.html')
    context = {
        'copia': copia,
        'socio': socio,
    }
    return HttpResponse(template.render(context, request))


def list_libros(request):
    if request.method == 'POST':
        isbn = request.POST.get('id', None)
        return info_libro(request, isbn)
    else: 
        libros_list = Libro.objects.all().order_by('titulo')
        template = loader.get_template('MSGB/listado_libros.html')
        context = {        
            'libros_list': libros_list,
        }
        return HttpResponse(template.render(context, request))

def list_copias(request):
    if request.method == 'POST':
        nro_inventario = request.POST.get('id', None)
        return info_copia(request, nro_inventario)
    else: 
        copias_list = Ejemplar.objects.all().order_by('num_inventario')
        template = loader.get_template('MSGB/listado_copias.html')
        context = {        
            'copias_list': copias_list,
        }
        return HttpResponse(template.render(context, request))

def morosos(request):
    morosos_list = Socio.objects.filter(moroso=True).order_by('documento')
    template = loader.get_template('MSGB/morosos.html')
    context = {        
        'morosos_list': morosos_list,
    }
    return HttpResponse(template.render(context, request))


def alta_socio(request):
    if request.method == "POST":
        form = SocioForm(request.POST)
        if form.is_valid():
            socio = form.save(commit=False)
            socio.save()
            return redirect("index")
    else:
        form = SocioForm()
        return render(request,'forms/alta_socios.html', {'form':form})


def futuros_morosos(request):
    mosoros_list = []    
    prestamo_list = Prestamo.objects.filter(devuelto=False).order_by('fecha_ini')
    if len(prestamo_list) > 0:    
        mosoros_list = list(filter(lambda x: x.fecha_ini + timedelta(days=7)< date.today(), prestamo_list))
    template = loader.get_template('MSGB/futuros_morosos.html')
    context = {        
        'morosos_list': mosoros_list,
    }
    return HttpResponse(template.render(context, request))

#def libros_prestados(doc_socio):
#        fecha = datetime.date.today()
#        for prestamo in Socio