"""URLs de views de la aplicación órdenes"""
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from ordenes.models import Orden
from ordenes.forms import OrdenForm
from django.urls import reverse_lazy
from django.shortcuts import render
from catalogos.models import *

class LoginView(auth_views.LoginView):
    """Vista de autenticacion"""
    template_name = 'ordenes/login.html'
    #redirect_field_name = 'next'

class LogoutView(auth_views.LogoutView):
	"""Vista de logout"""
	pass

class ListadoView(LoginRequiredMixin, ListView):
	"""Regresa el listado de ordenes"""
	template_name = 'ordenes/listado.html'
	model = Orden
	ordering = ('-fecha_inicio',)
	paginate_by = 10
	context_object_name= 'ordenes'

class NuevoView(LoginRequiredMixin, CreateView):
    """Crea nueva orden con CreateView"""
    template_name='ordenes/alta.html'
    form_class = OrdenForm
    model =  Orden
    success_url = reverse_lazy('ordenes:listado')

    def get_context_data(self, **kwargs):
        """Inserción de los catálogos de registros activos de gerencias, proveedores, localidades y servicios"""
        ctx = super(NuevoView, self).get_context_data(**kwargs)
        ctx['gerencias'] = Gerencia.objects.filter(activo = 1)
        ctx['proveedores'] = Proveedor.objects.filter(activo = 1)
        ctx['localidades'] = Localidad.objects.filter(activo = 1)
        ctx['servicios'] = Servicio.objects.filter(activo = 1)
        return ctx

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        model = form.save(commit=False)
        seguimiento = str(Orden.objects.filter(fecha_inicio=model.fecha_inicio).count() + 1).zfill(5)
        codigo_localidad = ""
        for localidad in form.cleaned_data['localidades']:
            codigo_localidad = localidad.codigo
            break
        codigo = model.actividad + "-" + model.proveedor.codigo + "-" + codigo_localidad + "-" + model.fecha_inicio.strftime('%Y%m%d') + "-" + str(seguimiento)
        model.id = codigo
        return super().form_valid(form)

def carga_actividad(request):
    """Función Ajax para mostrar el detalle de una actividad"""
    iden = request.GET.get('actividad')
    actividad = Orden.objects.get(pk = iden)
    return render(request,'ordenes/consulta.html',{'actividad': actividad })

def carga_submodulos(request):
    """Función usada por Ajax para actualizar los catálogos de supervisores, teléfonos de contacto y ejecutores"""
    movimiento = request.GET.get('movimiento')
    if movimiento == 'gerencia':
        gerencia_id = request.GET.get('gerencia_id')
        supervisor_elegido = request.GET.get('supervisor_id')
        supervisores = Supervisor.objects.filter(gerencia_id=gerencia_id, activo=1).order_by('nombre')
        return render(request, 'ordenes/lista_supervisores.html', {'supervisores': supervisores, 'elegido':supervisor_elegido})
    elif movimiento == 'supervisor':
        supervisor_id = request.GET.get('supervisor_id')
        supervisor = Supervisor.objects.get(id=supervisor_id)
        return render(request, 'ordenes/telefono.html', {'telefono': supervisor.telefono})
    elif movimiento == 'proveedor':
        proveedor_id = request.GET.get('proveedor_id')
        ejecutores_elegidos = request.GET.get('ejecutores').split(",")
        print("--lista ejecutores--")
        print(ejecutores_elegidos)
        ejecutores = Ejecutor.objects.filter(proveedor_id=proveedor_id, activo=1).order_by('nombre')
        return render(request, 'ordenes/lista_ejecutores.html', {'ejecutores': ejecutores , 'elegidos': ejecutores_elegidos})
