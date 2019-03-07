"""Clases middleware"""
from django.conf import settings
from django.shortcuts import redirect

class InactivityValidationMiddleware:
    """Clase middleware que resetea los 10 minutos de inactividad cada que
    se haga una actividad en la sesión, así como la protección de la carpeta
    de media en caso de no tener sesión abierta
    """
    def __init__(self, get_response):
        """Inicializacion"""
        self.get_response = get_response

    def __call__(self, request):
        """Ejecución de middleware"""
        """Validación de inactividad"""
        if not request.session.is_empty():
            request.session.set_expiry(request.session.get_expiry_age())
        else:
            """Protección de carpeta de media"""
            if request.path.startswith(settings.MEDIA_URL):
                return redirect('ordenes:login')
        response = self.get_response(request)
        return response
