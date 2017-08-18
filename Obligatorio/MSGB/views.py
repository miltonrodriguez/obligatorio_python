from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from datetime import  date, timedelta
from .models import Socio, Prestamo, Libro, Ejemplar
from .forms import DevolucionForm, PrestamoForm, SocioForm
from django.template import loader
import time



# Create your views here.

def index(request):
    template = loader.get_template('MSGB/index.html')
    return HttpResponse(template.render())

def prestamo(request):
    try:
        if request.method == "POST":
            form = PrestamoForm(request.POST)
            if form.is_valid():  
                error = None
                p = None
                id_socio = request.POST.get('socio', None)                    
                socio = get_object_or_404(Socio, pk=id_socio)
                if (socio.moroso == True):
                    error = 'El socion es moroso. No se le puede prestar libros.'
                else: 
                    id_libro = int(request.POST.get('libro', None))
                    libro = get_object_or_404(Libro, pk=id_libro)
                    copia = libro.ejemplar_set.all().order_by('-disponible').first()                    
                    if copia == None or copia.disponible == False:
                        error = 'No hay copias disponibles'
                    else:
                        copia.disponible = False
                        copia.save()                                       
                        p = Prestamo(ejemplar = copia, socio = socio, fecha_ini = date.today(), fecha_fin = date.today() + timedelta(days=7), devuelto = False)                        
                        p.save()                           
                template = loader.get_template('MSGB/prestamo.html')
                context = {
                    'error': error,
                    'p' : p,
                    
                }
                return HttpResponse(template.render(context, request))
        else:
            form = PrestamoForm()
            return render(request,'forms/prestamos_form.html', {'form':form})
    except Exception as e:
        error(request, e)
        

def devolucion(request):
    if request.method == "POST":
        form = DevolucionForm(request.POST)
        if form.is_valid():  
            msj = ''            
            id_socio = request.POST.get('socio', None)                            
            socio = get_object_or_404(Socio, pk=id_socio)
            num_inventario = int(request.POST.get('ejemplar', None))
            ejemplar = get_object_or_404(Ejemplar, pk=num_inventario)
            p = get_object_or_404(Prestamo,  ejemplar_id=num_inventario , socio_id = id_socio)
            #chequeo de moroso
            if not (p.fecha_ini + timedelta(days=7) > date.today()):                        
                # es moroso
                socio.moroso = True
                socio.save()
                msj =  "El socio devolvio el ejemplar fuera de fecha. "
            p.fecha_fin = date.today()
            p.devuelto = True
            p.save()                        
            ejemplar.disponible = True
            ejemplar.save()
            msj = msj + ' ' +  'Se devolvio con exito el ejemplar.'                
            template = loader.get_template('MSGB/devolver.html')
            context = {
                'msj': msj,                                
            }
            return HttpResponse(template.render(context, request))
    else:
        form = DevolucionForm()
        return render(request,'forms/devolver_form.html', {'form':form})

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
    socio, prestamo = None, None
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

def prestamo_fecha(request, fecha=''):
    fecha = request.GET.get('fecha', '')
    error = None
    results = []    
    try:        
        if (fecha != '' ): 
            es_valida = time.strptime(fecha, '%Y-%m-%d')
            results = Prestamo.objects.filter(fecha_ini = fecha)
    except Exception:        
        error = 'La fecha no cumple con el formato correcto'           
    template = loader.get_template('MSGB/prestamo_fecha.html')
    context = {        
        'fecha': fecha,
        'results' : results,
        'error' : error,
    }
    return HttpResponse(template.render(context, request))
    
def error(request,msj_error):        
    template = loader.get_template('MSGB/error.html')
    context = {        
        'error': msj_error,        
    }
    return HttpResponse(template.render(context, request))    



    