from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^prestamo/(?P<documento>[0-9]+)/(?P<isbn>[0-9]+)$', views.prestamo, name='prestamo'),
    url(r'^devolucion/(?P<documento>[0-9]+)/(?P<nro_inventario>[0-9]+)$', views.devolucion, name='devolucion'),
    url(r'^socio/(?P<documento>[0-9]+)$', views.info_socio, name='info_socio'),
    url(r'^copia/(?P<nro_inventario>[0-9]+)$', views.copia, name='copia'),
    #url(r'^libro/(?P<isbn>[0-9]+)$', views.libro, name='libro'),
    url(r'^morosos$', views.morosos, name='morosos'),
    #url(r'^prestamo_fecha/(?P<fecha>$', views.prestamo_fecha, name='prestamo_fecha'),
    #url(r'^futuros_morosos$', views.futuros_morosos$, name='futuros_morosos$'),
    
    url(r'^socio/nuevo/$', views.alta_socio, name='alta_socio'),
    
]