from django.shortcuts import render

# Create your views here.

from ServiciosApp.models import Servicio
from django.contrib.auth.decorators import login_required, permission_required


from django.contrib.auth.decorators import user_passes_test

# Define una función para verificar si el usuario es Editor_contenido
def es_editor_contenido(user):
    if not user.is_authenticated:
        return False  # Redirigir o denegar acceso si el usuario no está autenticado
    return user.tipo_usuario == 'Editor_contenido'

@user_passes_test(es_editor_contenido)
def servicios(request):

    servicios=Servicio.objects.all()
    return render(request, "ServiciosApp/servicios.html", {"servicios" : servicios})