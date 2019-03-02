"""URLs de views de la aplicación órdenes"""

from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView
from ordenes.models import Orden
from ordenes.forms import OrdenForm,OrdenEstatusForm
from django.urls import reverse_lazy
from django.shortcuts import render
from catalogos.models import *
from django.contrib.messages.views import SuccessMessageMixin
from datetime import datetime
from emails.views import send_email
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required



class LoginView(auth_views.LoginView):
    """Vista de autenticacion"""
    template_name = 'ordenes/login.html'


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

    def get_queryset(self, **kwargs):
        """Filtrado de consulta"""
        valor = self.request.GET.get('searchby', None)
        ordering = self.get_ordering()
        if valor:
            return Orden.objects.filter(id__contains=valor).order_by(*ordering)
        else:
            return Orden.objects.all().order_by(*ordering)


class OrdenUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Actualiza estatus de orden"""
    template_name='ordenes/consulta.html'
    model =  Orden
    form_class = OrdenEstatusForm
    slug_field = 'pk'
    slug_url_kwarg = 'pk'
    success_url = reverse_lazy('ordenes:listado')
    success_message = "Orden %(id)s actualizado exitosamente"

    def form_invalid(self, form):
        """Se debe conservar el log en pantalla si hay un errors"""
        contexto = self.get_context_data(form=form)
        if not contexto.get('viejo_log'):
            contexto['viejo_log'] = form.initial['log']
        return self.render_to_response(contexto)

    def form_valid(self, form):
        """Generación de log de cambios"""
        model = form.save(commit=False)
        estatus = {1 : "Aceptado", 2 : "Rechazado", 3:"En ejecución", 4: "Finalizada"}
        updatelog = "Usuario " + self.request.user.first_name + " " + self.request.user.last_name + " cambia estado a " + estatus[model.estatus]
        if model.log:
            updatelog += " comentando lo siguiente:\n" + model.log +"\n"
        model.log = updatelog + form.initial['log']
        send_email(self.request.user.username, "Actualización de orden " + model.id, updatelog)
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        """Formato para generar el mensaje de orden actualizada"""
        return self.success_message % dict(
            cleaned_data,
            id=self.object.id,
        )


class NuevoView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Crea nueva orden con CreateView"""
    template_name='ordenes/alta.html'
    form_class = OrdenForm
    model =  Orden
    success_url = reverse_lazy('ordenes:listado')
    success_message = "Orden %(id)s  creada exitosamente"

    @method_decorator(permission_required('ordenes.add_orden',reverse_lazy('ordenes:listado')))
    def dispatch(self, *args, **kwargs):
        """Función de inicio donde se requiere privilegios de alta"""
        return super(NuevoView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        """Inserción de los catálogos de registros activos de gerencias, proveedores, localidades y servicios"""
        ctx = super(NuevoView, self).get_context_data(**kwargs)
        ctx['gerencias'] = Gerencia.objects.filter(activo = 1)
        ctx['proveedores'] = Proveedor.objects.filter(activo = 1)
        ctx['localidades'] = Localidad.objects.filter(activo = 1)
        ctx['servicios'] = Servicio.objects.filter(activo = 1)
        return ctx

    def form_valid(self, form):
        """Guardado de nueva orden, el cual genera la clave de la actividad y log de creación"""
        model = form.save(commit=False)
        seguimiento = str(Orden.objects.filter(fecha_inicio=model.fecha_inicio).count() + 1).zfill(5)
        codigo_localidad = ""
        for localidad in form.cleaned_data['localidades']:
            codigo_localidad = localidad.codigo
            break
        codigo = model.actividad + "-" + model.proveedor.codigo + "-" + codigo_localidad + "-" + model.fecha_inicio.strftime('%Y%m%d') + "-" + str(seguimiento)
        model.id = codigo

        updatelog = "Orden creada por " + self.request.user.first_name + " " + self.request.user.last_name + " el día " + datetime.now().strftime("%d/%m/%Y a las %H:%M")+"\n"


        if model.log:
            model.log = updatelog + "Comentarios adicionales:\n" + model.log
        else:
            model.log = updatelog

        updatelog += "\nAsunto:" + model.asunto + "\nDetalle:\n" + model.detalle

        model.creador = self.request.user.username
        send_email(self.request.user.username, "Creación exitosa de orden " + model.id, updatelog)

        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        """Formato para generar el mensaje de orden creada y desliegue de código de órden"""
        return self.success_message % dict(
            cleaned_data,
            id=self.object.id,
        )


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
        ejecutores = Ejecutor.objects.filter(proveedor_id=proveedor_id, activo=1).order_by('nombre')
        return render(request, 'ordenes/lista_ejecutores.html', {'ejecutores': ejecutores , 'elegidos': ejecutores_elegidos})
