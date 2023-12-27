from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import View
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .forms import CustomUserCreationForm, UserProfileForm, EmpresaForm, UserAndEmpresaForm, CustomUserUpdateForm

from .models import CustomUser,Empresa

##csv##
import csv
from .forms import CSVUploadForm  # Importa el formulario para subir el CSV
from django.db import transaction
##csv##

# Create your views here.

def cerrar_sesion(request):
    logout(request)

    return redirect('Home')


def registro(request):
    if request.method == 'POST':
        form = UserAndEmpresaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            messages.success(request, "Te has registrado con éxito")
            return redirect(to="Home")
    else:
        form = UserAndEmpresaForm()

    return render(request, 'registration/registro.html', {'form': form})





from .forms import UserProfileForm

@login_required
def view_profile(request):
    user = request.user
    empresa_nombre = user.empresa.nombre_empresa if user.empresa else 'Sin empresa asignada'
    return render(request, 'registration/view_profile.html', {'user': user, 'empresa_nombre': empresa_nombre})



@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'registration/edit_profile.html', {'form': form})



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from .models import CustomUser
from django.contrib import messages

# Vista para crear un nuevo usuario personalizado
def crear_usuario_personalizado(request):
    if not request.user.is_authenticated:
        # Redirigir al usuario a la página de inicio de sesión si no está autenticado
        return redirect('login')  # Asegúrate de reemplazar esto con el nombre correcto de tu vista de inicio de sesión
    if request.method == 'POST':
        formulario = CustomUserCreationForm(request.POST, request.FILES, current_user=request.user)
        if formulario.is_valid():
            nuevo_usuario = formulario.save(commit=False)

            # Asociar la empresa seleccionada al usuario
            empresa_seleccionada = formulario.cleaned_data['nombre_empresa']
            if empresa_seleccionada:
                nuevo_usuario.empresa = empresa_seleccionada

            nuevo_usuario.save()

            send_mail(
            


            'contacto desde Kabasis', # subject
            # en el mensaje se envia una bienvenida junto a su usarname y contraseña
            'Bienvenido a Kabasis Web, \n\n'
            'Le informamos que ha sido inscrito en nuestra plataforma para certificarse. \n\n'
            'Sus credenciales de acceso son las siguientes: \n'
            f'Usuario: {formulario.cleaned_data["username"]} \n'
            f'Contraseña: {formulario.cleaned_data["password1"]} \n\n'
            'Le recomendamos cambiar su contraseña, la cual ha sido generada de manera aleatoria. '
            'Para ello, inicie sesión con la contraseña proporcionada y actualícela en la sección de configuración de su cuenta. \n\n'
            'Gracias por unirse a Kabasis Web. ¡Le deseamos mucho éxito en su certificación! \n\n'
            'Atentamente, \n'
            'El equipo de Kabasis Web', # message
            from_email=settings.EMAIL_HOST_USER, # from email
            # el destinatario es el email que se ha registrado
            recipient_list=[formulario.cleaned_data['email']], # recipient emails
            
            fail_silently=False
            )
            messages.success(request, 'Usuario creado con éxito.')
            return redirect('lista_usuarios_personalizados')
    else:
        formulario = CustomUserCreationForm(current_user=request.user)

    return render(request, 'registration/formulario_usuario.html', {'formulario': formulario})

# Vista para listar usuarios personalizados
from django.shortcuts import redirect

def lista_usuarios_personalizados(request):
    # Comprobar si el usuario está autenticado y es un Administrador o Administrador Kabasis
    if request.user.is_authenticated and request.user.tipo_usuario in ['Administrador', 'Administrador Kabasis']:
        # Filtrar usuarios por la empresa del administrador si es necesario
        if request.user.tipo_usuario == 'Administrador':
            usuarios = CustomUser.objects.filter(empresa=request.user.empresa)
        else:
            # Si es Administrador Kabasis, mostrar todos los usuarios
            usuarios = CustomUser.objects.all()
    else:
        # Si no es un usuario autorizado, redirigir al inicio de sesión
        return redirect('login')  # Asegúrate de reemplazar esto con el nombre correcto de tu vista de inicio de sesión

    return render(request, 'registration/lista_usuarios.html', {'usuarios': usuarios})



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import CustomUserUpdateForm
from .models import CustomUser

def actualizar_usuario_personalizado(request, id_usuario):
    usuario = get_object_or_404(CustomUser, pk=id_usuario)
    if request.method == 'POST':
        # Pasar el usuario actual al formulario
        formulario = CustomUserUpdateForm(request.POST, instance=usuario, current_user=request.user)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Usuario actualizado correctamente")
            return redirect('lista_usuarios_personalizados')
    else:
        # Pasar el usuario actual al formulario
        formulario = CustomUserUpdateForm(instance=usuario, current_user=request.user)

    return render(request, 'registration/formulario_usuario.html', {'formulario': formulario})


# Vista para eliminar un usuario personalizado
def eliminar_usuario_personalizado(request, id_usuario):
    if request.method == 'GET':
        usuario = get_object_or_404(CustomUser, id=id_usuario)
        usuario.delete()
        messages.success(request, 'Usuario eliminado con éxito.')
        return redirect('lista_usuarios_personalizados')
    return redirect('Home')


##########Empresas#################

# Vista para crear una nueva empresa
from django.shortcuts import redirect
from django.contrib import messages

def crear_empresa(request):
    # Comprobar si el usuario está autenticado y es un Administrador Kabasis
    if not (request.user.is_authenticated and request.user.tipo_usuario == 'Administrador Kabasis'):
        # Si no es Administrador Kabasis, redirigir al inicio de sesión
        return redirect('login')  # Reemplaza esto con el nombre de tu vista de inicio de sesión

    if request.method == 'POST':
        formulario = EmpresaForm(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Empresa creada con éxito.')
            return redirect('crear_empresa')  # Reemplaza esto con la ruta adecuada después de crear la empresa
        else: 
            data = {'form': formulario}
    else:
        data = {'form': EmpresaForm()}

    return render(request, "empresas/crear_empresa.html", data)


from django.shortcuts import redirect

def listar_empresa(request):
    # Comprobar si el usuario está autenticado y es un Administrador Kabasis
    if request.user.is_authenticated and request.user.tipo_usuario == 'Administrador Kabasis':
        empresas = Empresa.objects.all()
        data = {'empresas': empresas}
        return render(request, "empresas/listar_empresa.html", data)
    else:
        # Si no es Administrador Kabasis, redirigir al inicio de sesión
        return redirect('login')  # Reemplaza esto con el nombre correcto de tu vista de inicio de sesión



from django.shortcuts import redirect, get_object_or_404

def actualizar_empresa(request, id):
    # Comprobar si el usuario es Administrador Kabasis
    if not (request.user.is_authenticated and request.user.tipo_usuario == 'Administrador Kabasis'):
        return redirect('login')  # Reemplaza con el nombre de tu vista de inicio de sesión

    empresa = get_object_or_404(Empresa, id=id)
    data = {'form': EmpresaForm(instance=empresa)}

    if request.method == 'POST':
        formulario = EmpresaForm(data=request.POST, instance=empresa, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Empresa actualizada correctamente")
            return redirect(to="listar_empresa")
        
        data["form"] = formulario
    
    return render(request, "empresas/actualizar_empresa.html", data)


def eliminar_empresa(request, id):
    # Comprobar si el usuario es Administrador Kabasis
    if not (request.user.is_authenticated and request.user.tipo_usuario == 'Administrador Kabasis'):
        return redirect('login')  # Reemplaza con el nombre de tu vista de inicio de sesión

    empresa = get_object_or_404(Empresa, id=id)
    empresa.delete()
    messages.success(request, 'Empresa eliminada con éxito.')
    return redirect(to="listar_empresa")



def menu_administracion(request):
    
    return render(request, "empresas/menu_administracion.html")


######Creación de usuarios de manera masiva####


from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction, IntegrityError
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser, Empresa
from .forms import CSVUploadForm
import csv

def chunks(lst, n):
    """Divide la lista 'lst' en pedazos de tamaño 'n'."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

@transaction.atomic
def carga_masiva(request):
    usuarios_creados = 0
    usuarios_no_creados = 0
    usuarios_existente = []
    usuarios_empresa_inexistente = []
    created_users = []  # Lista para almacenar los usuarios creados
    BATCH_SIZE = 10  # Tamaño del lote

    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    csv_file = request.FILES['archivo_csv'].read().decode('utf-8')
                    csv_data = csv.reader(csv_file.splitlines())
                    data_list = list(csv_data)

                    emails_existentes = set()

                    # Procesamiento por lotes del archivo CSV
                    for chunk in chunks(data_list, BATCH_SIZE):
                        for row in chunk:
                            password, username, first_name, last_name, email, empresa_nombre = row[:6]
                            tipo_usuario = 'Estudiante'  # Establece el tipo de usuario por defecto

                            try:
                                empresa = Empresa.objects.get(nombre_empresa=empresa_nombre)
                            except Empresa.DoesNotExist:
                                usuarios_empresa_inexistente.append(username)
                                usuarios_no_creados += 1
                                continue

                            if CustomUser.objects.filter(email=email).exists():
                                usuarios_existente.append(email)
                                emails_existentes.add(email)
                                usuarios_no_creados += 1
                                continue

                            try:
                                new_user = CustomUser.objects.create(
                                    username=username,
                                    first_name=first_name,
                                    last_name=last_name,
                                    email=email,
                                    tipo_usuario=tipo_usuario,
                                    empresa=empresa
                                )
                                new_user.set_password(password)
                                new_user.save()
                                usuarios_creados += 1
                                created_users.append({
                                    'email': email,
                                    'username': username,
                                    'password': password
                                })
                            except IntegrityError:
                                usuarios_existente.append(username)
                                usuarios_no_creados += 1

                    # Envío de correos después de crear todos los usuarios
                    for user in created_users:
                        email = user['email']
                        subject = 'Contacto desde Kabasis'
                        message = (
                            'Bienvenido a Kabasis Web, \n\n'
                            'Le informamos que ha sido inscrito en nuestra plataforma para certificarse. \n\n'
                            'Sus credenciales de acceso son las siguientes: \n'
                            f'Usuario: {user["username"]} \n'
                            f'Contraseña: {user["password"]} \n\n'
                            'Le recomendamos cambiar su contraseña, la cual ha sido generada de manera aleatoria. '
                            'Para ello, inicie sesión con la contraseña proporcionada y actualícela en la sección de configuración de su cuenta. \n\n'
                            'Gracias por unirse a Kabasis Web. ¡Le deseamos mucho éxito en su certificación! \n\n'
                            'Atentamente, \n'
                            'El equipo de Kabasis Web'
                        )
                        from_email = settings.EMAIL_HOST_USER
                        recipient_list = [email]

                        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

                    # Mensajes según los resultados de la carga
                    if emails_existentes:
                        mensajes_correos = ", ".join(emails_existentes)
                        messages.warning(request, f'Se han creado {usuarios_creados} usuarios exitosamente. No se guardaron {usuarios_no_creados} usuarios debido a que los siguientes correos electrónicos ya existían: {mensajes_correos}.')
                    elif usuarios_existente:
                        messages.warning(request, f'Se han creado {usuarios_creados} usuarios exitosamente. No se guardaron {usuarios_no_creados} usuarios. Los siguientes usuarios ya existían y no se crearon: {", ".join(usuarios_existente)}')
                    elif usuarios_empresa_inexistente:
                        messages.warning(request, f'Se han creado {usuarios_creados} usuarios exitosamente. No se guardaron {usuarios_no_creados} usuarios. Los siguientes usuarios no se crearon por empresas inexistentes: {", ".join(usuarios_empresa_inexistente)}')
                    else:
                        messages.success(request, f'Se han creado {usuarios_creados} usuarios exitosamente.')
                        

                    return redirect('carga_masiva')

            except Exception as e:
                messages.error(request, f'Error general: {e}')

    else:
        form = CSVUploadForm()

    return render(request, 'registration/carga_masiva.html', {'form': form})




###################################
##Vista envío correo con invitación para el registro


import base64
from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib import messages
from .forms import EmailInvitationForm

import base64
from django.shortcuts import render
from django.contrib import messages
from .forms import EmailInvitationForm

def invitacion_email(request):
    id_empresa = request.user.empresa.id

    # Codificar el ID de la empresa en base64
    id_empresa_codificado = base64.urlsafe_b64encode(str(id_empresa).encode()).decode()

    # Incluye el ID de la empresa codificado en el enlace
    link_registro = f'http://192.168.1.38/autenticacion/form_invitacion/?empresa_id={id_empresa_codificado}'

    if request.method == 'POST':
        form = EmailInvitationForm(request.POST)
        if form.is_valid():
            email_destinatario = form.cleaned_data['email']

            # Mensaje de invitación adaptado
            mensaje_invitacion = (
                "Equipo,\n\n"
                "La protección de nuestra información es primordial. Te invito a descubrir una herramienta poderosa "
                "para expandir nuestros conocimientos en seguridad digital: Kabasis.\n\n"
                "Con cursos especializados y recursos de vanguardia, Kabasis es la puerta de entrada a una comprensión "
                "más profunda y actualizada de la ciberseguridad.\n\n"
                f"Regístrate hoy mismo en {link_registro} y sé parte de esta iniciativa que fortalecerá nuestro enfoque "
                "en la protección de datos.\n\n"
                "Nos vemos en Kabasis."
            )

            # Envío del correo con el mensaje de invitación
            send_mail(
                'Únete a la vanguardia en seguridad digital con Kabasis',
                mensaje_invitacion,
                'tu_email@ejemplo.com',
                [email_destinatario],
                fail_silently=False,
            )
            messages.success(request, 'Invitación enviada con éxito.')
            return redirect('invitacion_email')
    else:
        form = EmailInvitationForm()

    context = {
        'form': form,
        'link_registro': link_registro
    }
    return render(request, "registration/email_invitacion.html", context)






from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import UserAndEmpresaEmailForm
from .models import Empresa
import base64

def form_invitacion(request):
    # Obtiene el ID de la empresa codificado en base64 desde la URL
    empresa_id_encoded = request.GET.get('empresa_id')

    if empresa_id_encoded:
        # Intenta decodificar el ID de la empresa
        try:
            empresa_id = base64.urlsafe_b64decode(empresa_id_encoded.encode()).decode()
            empresa_id = int(empresa_id)  # Convierte el ID de empresa a entero
        except (ValueError, base64.binascii.Error):
            # Manejar el error si el valor no se puede decodificar correctamente
            messages.error(request, "Enlace de invitación inválido.")
            return redirect('ruta_a_alguna_vista')  # Reemplaza con la ruta a donde redirigir en caso de error
    else:
        messages.error(request, "No se proporcionó ID de empresa.")
        return redirect('ruta_a_alguna_vista')  # Reemplaza con la ruta a donde redirigir en caso de error

    if request.method == 'POST':
        form = UserAndEmpresaEmailForm(request.POST, request.FILES, empresa_id=empresa_id)
        if form.is_valid():
            user = form.save()

            # Autenticar y loguear al usuario
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            if user is not None:
                login(request, user)

            messages.success(request, "Te has registrado con éxito")
            return redirect('Home')  # Reemplaza con la ruta a donde redirigir después del registro exitoso
    else:
        form = UserAndEmpresaEmailForm(empresa_id=empresa_id)

    return render(request, 'registration/form_invitacion.html', {'form': form})
