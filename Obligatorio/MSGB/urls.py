from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^prestamo/', views.prestamo, name='prestamo'),
    url(r'^devolucion/', views.devolucion, name='devolucion'),
    url(r'^socio/(?P<documento>[0-9]+)$', views.info_socio, name='info_socio'),
    url(r'^list_socios$', views.list_socios, name='list_socio'),
    url(r'^copia/(?P<num_inventario>[0-9]+)$', views.info_copia, name='copia'),
    url(r'^list_copias$', views.list_copias, name='list_copias'),    
    url(r'^libro/(?P<isbn>[0-9]+)$', views.info_libro, name='libro'),    
    url(r'^list_libros$', views.list_libros, name='list_libros'),    
    url(r'^morosos$', views.morosos, name='morosos'),
    url(r'^prestamo_fecha/(?P<fecha>[0-9]+)*', views.prestamo_fecha, name='prestamo_fecha'),
    url(r'^futuros_morosos$', views.futuros_morosos, name='futuros_morosos$'),    
    url(r'^socio/nuevo/$', views.alta_socio, name='alta_socio'),
    
]