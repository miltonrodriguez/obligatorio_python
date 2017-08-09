from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
import datetime
from .models import Socio, Prestamo, Libro
from .forms import SocioForm
from builtins import int
from django.template import loader
from django.template.context_processors import request

# Create your views here.

def index(request):
    return redirect("index")

def prestamo(request):
    return redirect("index")

def devolucion(request):
    return redirect("index")

def info_socio(request, documento="3813973"):
    id = int(documento)
    socio = get_object_or_404(Socio, pk=id)
    prestamo_list = socio.prestamo_set.all()
    template = loader.get_template('MSGB/info_socio.html')
    context = {
        'socio': socio,
        'prestamo_list': prestamo_list,
    }
    return HttpResponse(template.render(context, request))

def copia(request):
    return redirect("index")







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

#def libros_prestados(doc_socio):
#        fecha = datetime.date.today()
#        for prestamo in Socio