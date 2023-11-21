from django.shortcuts import render, redirect,  get_object_or_404
from django.views.generic import View
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .forms import CustomUserCreationForm, UserProfileForm, EmpresaForm

from .models import CustomUser,Empresa

###CSV###
import csv
from .forms import CSVUploadForm  # Importa el formulario para subir el CSV
from django.db import transaction
from django.contrib.auth.hashers import make_password
###CSV###


# Create your views here.

def cerrar_sesion(request):
    logout(request)

    return redirect('Home')


def registro(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        formulario = CustomUserCreationForm(request.POST, request.FILES)
        if formulario.is_valid():
            # Guarda el usuario pero sin commit para poder manipularlo antes de guardar
            user = formulario.save(commit=False)
            
            # Ahora, obtén la empresa seleccionada del formulario
            empresa_id = request.POST.get('nombre_empresa')
            empresa = Empresa.objects.get(pk=empresa_id) if empresa_id else None
            
            # Asigna la empresa al usuario
            user.empresa = empresa
            
            # Guarda el usuario con la empresa asignada
            user.save()

            # Realiza el resto del proceso de autenticación y redirección
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)
            messages.success(request, "Te has registrado con éxito")
            return redirect(to="Home")
        
        data["form"] = formulario

    return render(request, 'registration/registro.html', data)


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


# Vista para crear un nuevo usuario personalizado
def crear_usuario_personalizado(request):
    if request.method == 'POST':
        formulario = CustomUserCreationForm(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Usuario creado con éxito.')
            return redirect('lista_usuarios_personalizados')
    else:
        formulario = CustomUserCreationForm()
    return render(request, 'registration/formulario_usuario.html', {'formulario': formulario})


# Vista para listar usuarios personalizados
def lista_usuarios_personalizados(request):
    usuarios = CustomUser.objects.all()
    return render(request, 'registration/lista_usuarios.html', {'usuarios': usuarios})

# Vista para actualizar un usuario personalizado
def actualizar_usuario_personalizado(request, id_usuario):
    usuario = get_object_or_404(CustomUser, pk=id_usuario)
    if request.method == 'POST':
        formulario = CustomUserCreationForm(request.POST, instance=usuario)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Usuario actualizado correctamente")
            return redirect('lista_usuarios_personalizados')
    else:
        formulario = CustomUserCreationForm(instance=usuario)
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

# Vista para crear un nuevo usuario personalizado
def crear_empresa(request):

    data = {
        'form': EmpresaForm()

    }

    if request.method == 'POST':
        formulario = EmpresaForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Empresa creada con éxito.')
        else: 
            data["form"] = formulario
    
    return render(request, "empresas/crear_empresa.html", data)

def listar_empresa(request):
    empresas = Empresa.objects.all()

    data = {
        'empresas': empresas
    }

    return render(request, "empresas/listar_empresa.html", data)


def actualizar_empresa(request, id):

    empresa = get_object_or_404(Empresa, id=id)

    data= {
        'form': EmpresaForm(instance = empresa)
    }

    if request.method == 'POST':
        formulario = EmpresaForm(data=request.POST, instance=empresa, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Empresa actualizada correctamente")
            return redirect(to="listar_empresa")
        
        data["form"] = formulario
    
    return render(request, "empresas/actualizar_empresa.html", data)

def eliminar_empresa(request, id):
    curso = get_object_or_404(Empresa, id=id)
    curso.delete()
    messages.success(request, 'Empresa eliminada con éxito.')
    return redirect(to="listar_empresa")


def menu_administracion(request):
    
    return render(request, "empresas/menu_administracion.html")



##carga masiva de usuarios##


@transaction.atomic
def carga_masiva(request):
    usuarios_creados = 0
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['archivo_csv'].read().decode('utf-8')
            csv_data = csv.reader(csv_file.splitlines())

            # Itera sobre cada fila del CSV para crear los usuarios
            for row in csv_data:
                password, username, first_name, last_name, email, tipo_usuario = row[:6]  # Ajusta según tu CSV

                # Crea un nuevo usuario con los datos del CSV
                new_user = CustomUser.objects.create(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    tipo_usuario=tipo_usuario
                )

                # Usa set_password para cifrar y guardar la contraseña
                new_user.set_password(password)
                new_user.save()

                usuarios_creados += 1  # Incrementa el contador

            # Muestra el mensaje de éxito con la cantidad de usuarios creados
            messages.success(request, f'Se han creado {usuarios_creados} usuarios exitosamente.')

            # Redirige después de cargar los usuarios
            return redirect('carga_masiva')
    else:
        form = CSVUploadForm()  # Si no es un POST, muestra el formulario en blanco

    return render(request, 'registration/carga_masiva.html', {'form': form})