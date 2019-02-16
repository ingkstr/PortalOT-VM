from django.contrib import admin
from catalogos.models import *


class NoDeletableModelAdmin(admin.ModelAdmin):
    """Clase ModelAdmin sin la capacidad de eliminar registros"""
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Supervisor)
class SupervisorAdmin(NoDeletableModelAdmin):
    """Clase NoDeletableModelAdmin para el supervisor"""
    list_display = ('pk','nombre','telefono','gerencia','activo',)
    list_display_links = ('pk',)
    search_fields = ('nombre','telefono','gerencia','activo',)
    list_editable = ('nombre','telefono','gerencia','activo',)
    verbose_name_plural= 'Supervisores'

    fieldsets=(
            ('Información',{
                'fields':(('nombre', 'telefono'),),
                }),
            ('Gerencia',{
                'fields':(( 'gerencia', ),),
                }),
            ('Status',{
                'fields':(( 'activo', ),),
                }),
        )

class SupervisorInline(admin.StackedInline):
	"""Permite crear supervisores en una gerencia"""
	model = Supervisor
	can_delete = False
	verbose_name_plural= 'Supervisores'

@admin.register(Gerencia)
class GerenciaAdmin(NoDeletableModelAdmin):
    """Clase NoDeletableModelAdmin para las gerencias"""
    inlines =  (SupervisorInline,)
    list_display = ('pk','nombre','activo',)
    list_display_links = ('pk',)
    search_fields = ('nombre','activo',)
    list_editable = ('nombre','activo',)
    verbose_name_plural= 'Gerencias'

    fieldsets=(
            ('Información',{
                'fields':(('nombre'),),
                }),
            ('Status',{
                'fields':(( 'activo', ),),
                }),
        )

@admin.register(Localidad)
class LocalidadAdmin(NoDeletableModelAdmin):
    """Clase NoDeletableModelAdmin para las localidades"""
    list_display = ('clli','localidad','activo',)
    list_display_links = ('clli',)
    search_fields = ('clli','localidad''activo',)
    list_editable = ('activo',)
    verbose_name_plural= 'Localidades'

    fieldsets=(
            ('Información',{
                'fields':(('clli'),('localidad'),),
                }),
            ('Ubicación',{
                'fields':(('ubicacion'),),
                }),
            ('Status',{
                'fields':(( 'activo', ),),
                }),
        )



@admin.register(Ejecutor)
class EjecutorAdmin(NoDeletableModelAdmin):
    """Clase NoDeletableModelAdmin para los ejecutores de los proveedores"""
    list_display = ('pk','nombre','proveedor','activo',)
    list_display_links = ('pk',)
    search_fields = ('nombre','proveedor','activo',)
    list_editable = ('nombre','proveedor','activo',)
    verbose_name_plural= 'Ejecutores'

    fieldsets=(
            ('Información',{
                'fields':(('nombre', ),),
                }),
            ('Proveedor',{
                'fields':(( 'proveedor', ),),
                }),
            ('Status',{
                'fields':(( 'activo', ),),
                }),
        )

class EjecutorInline(admin.StackedInline):
	"""Permite crear ejecutores en un proveedor"""
	model = Ejecutor
	can_delete = False
	verbose_name_plural= 'Ejecutores'


@admin.register(Proveedor)
class ProveedorAdmin(NoDeletableModelAdmin):
    """Clase NoDeletableModelAdmin para los proveedores"""
    inlines =  (EjecutorInline,)
    list_display = ('pk','nombre','codigo','activo',)
    list_display_links = ('pk',)
    search_fields = ('nombre','activo',)
    list_editable = ('nombre','activo',)
    verbose_name_plural= 'Proveedores'

    fieldsets=(
            ('Información',{
                'fields':(('nombre', 'codigo'),),
                }),
            ('Status',{
                'fields':(( 'activo', ),),
                }),
        )

@admin.register(Servicio)
class ServicioAdmin(NoDeletableModelAdmin):
    """Clase NoDeletableModelAdmin para los servicios"""
    list_display = ('pk','nombre','activo',)
    list_display_links = ('pk',)
    search_fields = ('nombre','activo',)
    list_editable = ('nombre','activo',)
    verbose_name_plural= 'Servicios'

    fieldsets=(
            ('Información',{
                'fields':(('nombre'),),
                }),
            ('Status',{
                'fields':(( 'activo', ),),
                }),
        )
