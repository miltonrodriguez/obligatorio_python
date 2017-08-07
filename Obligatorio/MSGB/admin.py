from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Libro
admin.site.register(Libro)

from .models import Ejemplar
admin.site.register(Ejemplar)

from .models import Socio
admin.site.register(Socio)

from .models import Prestamo
admin.site.register(Prestamo)