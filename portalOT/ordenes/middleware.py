"""Clases middleware"""


class InactivityValidationMiddleware:
    """Clase middleware que resetea los 10 minutos de inactividad cada que se haga una actividad en la sesión"""
    def __init__(self, get_response):
        """Inicializacion"""
        self.get_response = get_response

    def __call__(self, request):
        """Ejecución de middleware"""
        request.session.set_expiry(request.session.get_expiry_age())
        response = self.get_response(request)
        return response
